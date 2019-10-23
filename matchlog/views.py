from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from trueskill import TrueSkill

from matchlog.models import Match, MatchPlayer, Player
from matchlog.serializers import UserSerializer, PlayerSerializer, MatchPlayerSerializer, MatchSerializer, MatchResultSerializer, MatchupSerializer
from matchlog.permissions import IsHistoricallySafe


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all().order_by("-date_joined")
  serializer_class = UserSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = PlayerSerializer

  def get_queryset(self):
    queryset = Player.objects.all().order_by("id")
    user_ids = self.request.query_params.getlist("user.id")
    if len(user_ids) > 0:
      queryset = queryset.filter(user__id__in=user_ids)
    player_ids = self.request.query_params.getlist("id")
    if len(player_ids) > 0:
      queryset = queryset.filter(id__in=player_ids)
    return queryset

  @action(detail=False)
  def matchmake(self, request):
    queryset = self.get_queryset()
    # paginate matchups, not players!
    # so all players are part of the matchmaking pool
    # (this consumes a lot of resources regardless of page size)
    serializer = MatchupSerializer(queryset)
    page = self.paginate_queryset(serializer.data)
    return self.get_paginated_response(page)


class MatchPlayerViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = MatchPlayerSerializer

  def get_queryset(self):
    queryset = MatchPlayer.objects.all().order_by("-id")
    user_id = self.request.query_params.get("player.user.id")
    if user_id is not None:
      queryset = queryset.filter(player__user__id=user_id)
    return queryset


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
  permission_classes = [IsHistoricallySafe]
  queryset = Match.objects.all().order_by("-created")
  serializer_class = MatchSerializer

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class MatchResultViewSet(viewsets.ModelViewSet):
  permission_classes = [IsHistoricallySafe]
  queryset = Match.objects.all().order_by("-created")
  serializer_class = MatchResultSerializer

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
