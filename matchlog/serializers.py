from django.contrib.auth.models import User
from rest_framework import serializers
from trueskill import TrueSkill
import itertools
import math

from matchlog.models import Match, Player, MatchPlayer, MatchTeam


def win_probability(env, team1, team2):
    '''
    @return win probability for team 1
    '''
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (env.beta * env.beta) + sum_sigma)
    return env.cdf(delta_mu / denom)


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('url', 'id', 'username', 'password')
    extra_kwargs = {
      'password': {'write_only': True},
    }

  def create(self, validated_data):
    user = super(UserSerializer, self).create(validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user


class PlayerSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  rating = serializers.ReadOnlyField()

  class Meta:
    model = Player
    fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source="owner.id")

  class Meta:
    model = Match
    fields = '__all__'


class MatchResultSerializer(serializers.BaseSerializer):
  def to_internal_value(self, data):
    home_score = data.get("home_score")
    away_score = data.get("away_score")
    home_players = data.get("home_players")
    away_players = data.get("away_players")

    if not home_score:
      raise serializers.ValidationError({
        "home_score": "This field is required."
      })
    if not away_score:
      raise serializers.ValidationError({
        "away_score": "This field is required."
      })
    if not home_players:
      raise serializers.ValidationError({
        "home_players": "This field is required."
      })
    if not away_players:
      raise serializers.ValidationError({
        "away_players": "This field is required."
      })

    return {
      "home_score": home_score,
      "away_score": away_score,
      "home_players": home_players,
      "away_players": away_players,
    }

  def to_representation(self, instance):
    home_team, away_team = MatchTeam.objects.filter(match=instance)
    home_players = MatchPlayer.objects.filter(team=home_team)
    away_players = MatchPlayer.objects.filter(team=away_team)
    return {
      "id": instance.id,
      "created": instance.created,
      "owner": instance.owner.id,
      "home_players": [mp.player_id for mp in home_players],
      "away_players": [mp.player_id for mp in away_players],
      "home_score": home_team.score,
      "away_score": away_team.score,
    }

  def create(self, data):
    match = Match(owner=data["owner"])
    match.save()

    home_score = data["home_score"]
    away_score = data["away_score"]

    home_team = MatchTeam(index=0, score=home_score, match=match)
    home_team.save()
    away_team = MatchTeam(index=1, score=away_score, match=match)
    away_team.save()

    # load players from database
    home_players = data["home_players"]
    away_players = data["away_players"]

    home_players = [Player.objects.get(id=p) for p in home_players]
    away_players = [Player.objects.get(id=p) for p in away_players]

    # copy pre-match ratings to MatchPlayer
    home_players = [MatchPlayer(
      player=p, rating_mu=p.rating_mu, rating_sigma=p.rating_sigma, team=home_team)
      for p in home_players]
    for p in home_players:
      p.save()

    away_players = [MatchPlayer(
      player=p, rating_mu=p.rating_mu, rating_sigma=p.rating_sigma, team=away_team)
      for p in away_players]
    for p in away_players:
      p.save()

    # calculate TrueSkill ratings
    env = TrueSkill()

    home_ratings = [env.create_rating(
      mu=p.rating_mu, sigma=p.rating_sigma)
      for p in home_players
    ]
    away_ratings = [env.create_rating(
      mu=p.rating_mu, sigma=p.rating_sigma)
      for p in away_players
    ]

    draw = home_score == away_score
    home_won = home_score > away_score

    rating_groups = [home_ratings, away_ratings]
    if draw:
      ranks = [0, 0]
    else:
      ranks = [0 if home_won else 1, 1 if home_won else 0]

    # rate
    rating_groups = env.rate(rating_groups, ranks)

    # store new ratings on Player
    home_ratings = rating_groups[0]
    away_ratings = rating_groups[1]

    for index, rating in enumerate(home_ratings):
      p = home_players[index]
      p.player.rating_mu = rating.mu
      p.player.rating_sigma = rating.sigma
      p.player.save()

    for index, rating in enumerate(away_ratings):
      p = away_players[index]
      p.player.rating_mu = rating.mu
      p.player.rating_sigma = rating.sigma
      p.player.save()

    return match


class MatchTeamSerializer(serializers.ModelSerializer):
  match = MatchSerializer(read_only=True)

  class Meta:
    model = MatchTeam
    fields = '__all__'


class MatchPlayerSerializer(serializers.ModelSerializer):
  player = PlayerSerializer(read_only=True)
  team = MatchTeamSerializer(read_only=True)
  rating = serializers.ReadOnlyField()

  class Meta:
    model = MatchPlayer
    fields = '__all__'


class MatchupSerializer(serializers.ListSerializer):
  child = PlayerSerializer()

  def to_representation(self, data):
    players = data
    env = TrueSkill()
    possible_teams = itertools.combinations_with_replacement(players, 2)
    possible_teams = [set(t) for t in possible_teams]
    possible_matchups = itertools.combinations(possible_teams, 2)
    all_players_distinct = lambda h, a: len(set(h) - set(a)) == len(set(h))
    possible_matchups = [(h, a) for h, a in possible_matchups if all_players_distinct(h, a)]
    matchup_qualities = []

    for home_players, away_players in possible_matchups:
      home_ratings = [env.create_rating(
        mu=p.rating_mu, sigma=p.rating_sigma)
        for p in home_players
      ]
      away_ratings = [env.create_rating(
        mu=p.rating_mu, sigma=p.rating_sigma)
        for p in away_players
      ]
      rating_groups = [home_ratings, away_ratings]

      quality = env.quality(rating_groups)
      win_probability_home = win_probability(env, home_ratings, away_ratings)

      home_ids = [p.id for p in home_players]
      away_ids = [p.id for p in away_players]
      matchup_qualities.append({
        "teams": [home_ids, away_ids],
        "win_probability": [win_probability_home, 1 - win_probability_home],
        "quality": quality
      })

    matchup_qualities = sorted(matchup_qualities,
      key=lambda m: m["quality"], reverse=True)
    return matchup_qualities