from matchlog.models import Match, Player
from django.contrib.auth.models import User
from rest_framework import viewsets
from matchlog.serializers import UserSerializer, PlayerSerializer, MatchSerializer

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer


class PlayerViewSet(viewsets.ModelViewSet):
  queryset = Player.objects.all().order_by('id')
  serializer_class = PlayerSerializer


class MatchViewSet(viewsets.ModelViewSet):
  queryset = Match.objects.all().order_by('-created')
  serializer_class = MatchSerializer
