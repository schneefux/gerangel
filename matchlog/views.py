from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from matchlog.models import Match, Player
from matchlog.serializers import UserSerializer, PlayerSerializer, MatchSerializer, MatchResultSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all().order_by("-date_joined")
  serializer_class = UserSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = PlayerSerializer

  def get_queryset(self):
    queryset = Player.objects.all().order_by("id")
    userid = self.request.query_params.get("user.id")
    if userid is not None:
      queryset = queryset.filter(user__id=userid)
    return queryset


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Match.objects.all().order_by("-created")
  serializer_class = MatchSerializer

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class MatchResultViewSet(viewsets.ModelViewSet):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  queryset = Match.objects.all().order_by("-created")
  serializer_class = MatchResultSerializer

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)