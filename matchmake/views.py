from rest_framework import viewsets
from matchlog.models import Player
from matchmake.serializers import MatchupSerializer

class MatchmakeViewSet(viewsets.GenericViewSet):
  def get_queryset(self):
    queryset = Player.objects.all().order_by("id")
    user_ids = self.request.query_params.getlist("user.id")
    if len(user_ids) > 0:
      queryset = queryset.filter(user__id__in=user_ids)
    player_ids = self.request.query_params.getlist("id")
    if len(player_ids) > 0:
      queryset = queryset.filter(id__in=player_ids)
    return queryset

  def list(self, request):
    queryset = self.get_queryset()
    # paginate matchups, not players!
    # so all players are part of the matchmaking pool
    # (this consumes a lot of resources regardless of page size)
    serializer = MatchupSerializer(queryset)
    page = self.paginate_queryset(serializer.data)
    return self.get_paginated_response(page)