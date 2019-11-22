from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from event.models import Event, Log
from event.serializers import EventSerializer, LogSerializer
from matchlog.models import Player


class EventViewSet(viewsets.ModelViewSet):
  queryset = Event.objects.all().order_by("-created")
  serializer_class = EventSerializer

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

  @action(detail=True)
  def match_result(self, request, pk=None):
    event = self.get_object()

    # order of players, colors, etc. is important
    players = set()
    colors = set()
    positions = set()
    player_color = dict()
    player_position = dict()
    player_goals = dict()
    team_scores = dict()
    team_id = dict()
    sets = []

    for log in event.log_set.all():
      player = log.player.id
      players.add(player)
      if log.action == "change_color":
        colors.add(log.payload)
        player_color[player] = log.payload
      if log.action == "change_position":
        positions.add(log.payload)
        player_position[player] = log.payload
      if log.action == "score_goal":
        player_goals[player] = player_goals.get(player, 0) + 1
      if log.action == "close_set":
        # split players into teams based on colors
        colors = list(colors)
        teams = [
          [
            p for p in players
            if player_color[p] == colors[n]
          ] for n in range(len(colors))
        ]
        # assign 'home' or 'away' (once) or retrieve
        # assumes players do not join/leave a team mid play
        team0_id = ",".join(str(i) for i in teams[0])
        team1_id = ",".join(str(i) for i in teams[1])
        if len(team_id) == 0:
          team_id[team0_id] = "home"
          team_id[team1_id] = "away"
        team0 = team_id[team0_id]
        team1 = team_id[team1_id]

        # assign scores
        team0_points = sum([player_goals.get(p, 0) for p in teams[0]])
        team1_points = sum([player_goals.get(p, 0) for p in teams[1]])
        if team0_points > team1_points:
          team_scores[team0] = team_scores.get(team0, 0) + 1
        if team0_points == team1_points:
          team_scores[team0] = team_scores.get(team0, 0) + 1
          team_scores[team1] = team_scores.get(team1, 0) + 1
        if team0_points < team1_points:
          team_scores[team1] = team_scores.get(team1, 0) + 1

        # reset!
        player_goals = dict()

        sets.append({
          team0 + "_color": colors[0],
          team1 + "_color": colors[1],
          team0 + "_points": team0_points,
          team1 + "_points": team1_points,
          team0 + "_positions": [player_position[p] for p in teams[0]],
          team1 + "_positions": [player_position[p] for p in teams[1]],
        })

    # use data from last set
    teams = [{
      "id": colors[0],
      "players": teams[0],
      "score": team_scores[team0],
    }, {
      "id": colors[1],
      "players": teams[1],
      "score": team_scores[team1],
    }]

    match_result = {
      "teams": teams,
      "sets": sets,
    }
    return Response(match_result)


class LogViewSet(viewsets.ModelViewSet):
  queryset = Log.objects.all().order_by("-created")
  serializer_class = LogSerializer

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
