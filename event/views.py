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
    colors = list()
    positions = set()
    player_color = dict()
    player_position = dict()
    player_goals = dict()
    team_id = dict()
    sets = []
    current_set = dict()

    def get_team_ids(team_map, players, colors):
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
      if len(team_map) == 0:
        team_map[team0_id] = "home"
        team_map[team1_id] = "away"
      team0 = team_map[team0_id]
      team1 = team_map[team1_id]

      return team0, team1, teams

    for log in event.log_set.all():
      player = log.player.id
      players.add(player)
      if log.action == "change_color":
        if log.payload not in colors:
          colors.append(log.payload)
        player_color[player] = log.payload
      if log.action == "change_position":
        positions.add(log.payload)
        player_position[player] = log.payload
      if log.action == "score_goal":
        team0, team1, teams = get_team_ids(team_id, players, colors)
        if log.player.id in teams[0]:
          current_set[team0 + "_points"] = current_set[team0 + "_points"] + 1
        if log.player.id in teams[1]:
          current_set[team1 + "_points"] = current_set[team1 + "_points"] + 1

      if log.action == "start_set":
        # reset data
        player_goals = dict()
        team0, team1, teams = get_team_ids(team_id, players, colors)
        current_set = {
          team0 + "_color": colors[0],
          team1 + "_color": colors[1],
          team0 + "_points": 0,
          team1 + "_points": 0,
          team0 + "_positions": [player_position[p] for p in teams[0]],
          team1 + "_positions": [player_position[p] for p in teams[1]],
        }

      if log.action == "close_set":
        sets.append(current_set)
        current_set = dict()

    if len(current_set) > 0:
      # auto close last
      sets.append(current_set)

    # calculate scores
    team_scores = dict()
    team_scores[team0] = 0
    team_scores[team1] = 0
    for s in sets:
      if s[team0 + "_points"] > s[team1 + "_points"]:
        team_scores[team0] = team_scores[team0] + 1
      if s[team0 + "_points"] == s[team1 + "_points"]:
        team_scores[team0] = team_scores[team0] + 1
        team_scores[team1] = team_scores[team1] + 1
      if s[team0 + "_points"] < s[team1 + "_points"]:
        team_scores[team1] = team_scores[team1] + 1

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
  serializer_class = LogSerializer

  def get_queryset(self):
    queryset = Log.objects.all().order_by("created")
    event_ids = self.request.query_params.getlist("event.id")
    if len(event_ids) > 0:
      queryset = queryset.filter(event__id__in=event_ids)
    gt_id = self.request.query_params.get("id_gt")
    if gt_id is not None:
      queryset = queryset.filter(id__gt=gt_id)
    return queryset

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
