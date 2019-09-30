from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.response import Response
from trueskill import TrueSkill

from matchlog.models import Match, Player, MatchTeam, MatchPlayer
from matchlog.serializers import UserSerializer, PlayerSerializer, MatchSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Player.objects.all().order_by('id')
  serializer_class = PlayerSerializer


class MatchViewSet(viewsets.ModelViewSet):
  queryset = Match.objects.all().order_by('-created')
  serializer_class = MatchSerializer

  def create(self, request):
    data = request.data
    match = Match()
    match.save()

    home_score = data.pop("home_score")
    away_score = data.pop("away_score")

    home_team = MatchTeam(index=0, score=home_score, match=match)
    home_team.save()
    away_team = MatchTeam(index=0, score=away_score, match=match)
    away_team.save()

    # load players from database
    home_players = data.pop("home_players")
    away_players = data.pop("away_players")

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

    return Response(status=status.HTTP_201_CREATED)