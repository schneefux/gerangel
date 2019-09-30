from matchlog.models import Match, Player, MatchPlayer, MatchTeam
from django.contrib.auth.models import User
from rest_framework import serializers
from trueskill import TrueSkill

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('url', 'id', 'username')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Player
    fields = '__all__'


class MatchSerializer(serializers.HyperlinkedModelSerializer):
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
    # TODO
    return {
    }

  def create(self, data):
    match = Match()
    match.save()

    home_score = data["home_score"]
    away_score = data["away_score"]

    home_team = MatchTeam(index=0, score=home_score, match=match)
    home_team.save()
    away_team = MatchTeam(index=0, score=away_score, match=match)
    away_team.save()

    # load players from database
    home_players = data["home_players"]
    away_players = data["away_players"]

    home_players = [Player.objects.get(id=p) for p in home_players]
    away_players = [Player.objects.get(id=p) for p in away_players]

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
      ranks = [1 if home_won else 0, 0 if home_won else 1]

    # rate
    rating_groups = env.rate(rating_groups, ranks)

    # store new ratings
    home_ratings = rating_groups[0]
    away_ratings = rating_groups[1]

    for index, rating in enumerate(home_ratings):
      p = home_players[index]
      p.rating_mu = rating.mu
      p.rating_sigma = rating.sigma
      p.save()

    for index, rating in enumerate(away_ratings):
      p = away_players[index]
      p.rating_mu = rating.mu
      p.rating_sigma = rating.sigma
      p.save()

    return True


class MatchTeamSerializer(serializers.HyperlinkedModelSerializer):
  match = MatchSerializer(read_only=True)

  class Meta:
    model = MatchTeam
    fields = '__all__'


class MatchPlayerSerializer(serializers.HyperlinkedModelSerializer):
  player = PlayerSerializer(read_only=True)
  team = MatchTeamSerializer(read_only=True)

  class Meta:
    model = MatchPlayer
    fields = '__all__'

