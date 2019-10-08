import itertools
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from trueskill import TrueSkill

from matchlog.models import Match, Player
from matchlog.serializers import UserSerializer, PlayerSerializer, MatchSerializer, MatchResultSerializer
from matchlog.permissions import IsHistoricallySafe


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

  @action(detail=False)
  def matchmake(self, request):
    # TODO add pagination
    players = self.get_queryset()
    env = TrueSkill()
    # TODO add 1v1 and 1v2
    possible_teams = itertools.combinations(players, 2)
    possible_matchups = itertools.combinations(possible_teams, 2)
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

      home_ids = [p.id for p in home_players]
      away_ids = [p.id for p in away_players]
      matchup_qualities.append({
        "teams": [home_ids, away_ids],
        "quality": quality
      })

    matchup_qualities = sorted(matchup_qualities,
      key=lambda m: m["quality"], reverse=True)
    return Response(matchup_qualities)


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