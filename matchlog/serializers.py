from matchlog.models import Match, Player
from django.contrib.auth.models import User
from rest_framework import serializers
from trueskill import Rating

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
    rating = Rating()

    user_data = validated_data.pop('user')
    user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    player, created = Player.objects.update_or_create(user=user, rating_mu=rating.mu, rating_sigma=rating.sigma)

    return player


class MatchSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Match
    fields = ('url', 'in_progress', 'home_player', 'home_score', 'away_player', 'away_score', 'created')
