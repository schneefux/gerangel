from matchlog.models import Match, Player, MatchPlayer, MatchTeam
from django.contrib.auth.models import User
from rest_framework import serializers

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


class MatchTeamSerializer(serializers.HyperlinkedModelSerializer):
  match = MatchSerializer(read_only=True)

  class Meta:
    model = MatchTeam
    fields = ('__all__')


class MatchPlayerSerializer(serializers.HyperlinkedModelSerializer):
  player = PlayerSerializer(read_only=True)
  team = MatchTeamSerializer(read_only=True)

  class Meta:
    model = MatchPlayer
    fields = ('__all__')

