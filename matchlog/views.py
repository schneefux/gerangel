from django.contrib.auth.models import User
from rest_framework import viewsets

from matchlog.models import Match, Player
from matchlog.serializers import UserSerializer, PlayerSerializer, MatchSerializer, MatchResultSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Player.objects.all().order_by('id')
  serializer_class = PlayerSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Match.objects.all().order_by('-created')
  serializer_class = MatchSerializer


class MatchResultViewSet(viewsets.ModelViewSet):
  queryset = Match.objects.all().order_by('-created')
  serializer_class = MatchResultSerializer