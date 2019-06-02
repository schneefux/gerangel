from matchlog.models import Match, Player
from django.contrib.auth.models import User
from rest_framework import serializers
from trueskill import TrueSkill

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('url', 'username', 'email', 'groups')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Player
    fields = ('url', 'user', 'rating_mu', 'rating_sigma')
    read_only_fields = ('rating_mu', 'rating_sigma')

  def create(self, validated_data):
    user_data = validated_data.pop('user')
    user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    player, created = Player.objects.update_or_create(user=user)
    return player


class MatchSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Match
    fields = ('url', 'in_progress', 'home_players', 'home_score', 'away_players', 'away_score', 'created')

  def create(self, validated_data):
    env = TrueSkill()
    match = super(MatchSerializer, self).create(validated_data)

    home_players = match.home_players.all()
    away_players = match.away_players.all()
    home_score = match.home_score
    away_score = match.away_score

    # create trueskill data structures
    home_ratings = [
      env.create_rating(
        mu=player.rating_mu,
        sigma=player.rating_sigma)
      for player in home_players
    ]
    away_ratings = [
      env.create_rating(
        mu=player.rating_mu,
        sigma=player.rating_sigma)
      for player in away_players
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
      player = home_players[index]
      player.rating_mu = rating.mu
      player.rating_sigma = rating.sigma
      player.save()

    for index, rating in enumerate(away_ratings):
      player = away_players[index]
      player.rating_mu = rating.mu
      player.rating_sigma = rating.sigma
      player.save()

    return match
