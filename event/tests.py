from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from matchlog.serializers import MatchResultSerializer
from matchlog.models import Player
from event.models import Event, Log


class EventTests(APITestCase):
  def setUp(self):
    self._test1 = User.objects.create_user(username="test1", password="test1")
    User.objects.create_user(username="test2", password="test2")
    User.objects.create_user(username="test3", password="test3")
    User.objects.create_user(username="test4", password="test4")
    self._event1 = Event.objects.create(owner=self._test1)
    self.client.login(username="test1", password="test1")

  def test_should_start_event(self):
    url = reverse("events-list")

    response = self.client.post(url, { })

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn("id", response.data)

  def test_should_add_entry_to_event(self):
    url = reverse("log-list")

    response = self.client.post(url, {
      "event": self._event1.id,
      "player": self._test1.id,
      "action": "change_color",
      "payload": "red",
    })

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_should_convert_to_matchresult(self):
    url = reverse("events-match-result", args=(self._event1.id,))
    create_event = lambda action, player, payload = "": Log.objects.create(
      event=self._event1, owner=self._test1, action=action,
      player=player, payload=payload)
    Pl = lambda pk: Player.objects.get(pk=pk)

    create_event(action="change_color", player=Pl(1), payload="red")
    create_event(action="change_color", player=Pl(2), payload="red")
    create_event(action="change_color", player=Pl(3), payload="blue")
    create_event(action="change_color", player=Pl(4), payload="blue")
    create_event(action="change_position", player=Pl(1), payload="attack")
    create_event(action="change_position", player=Pl(2), payload="defense")
    create_event(action="change_position", player=Pl(3), payload="attack")
    create_event(action="change_position", player=Pl(4), payload="defense")
    create_event(action="score_goal", player=Pl(1))
    create_event(action="score_goal", player=Pl(1))
    create_event(action="score_goal", player=Pl(3))
    create_event(action="close_set", player=Pl(1))
    create_event(action="score_goal", player=Pl(1))
    create_event(action="score_goal", player=Pl(3))
    create_event(action="score_goal", player=Pl(3))
    create_event(action="close_set", player=Pl(1))
    create_event(action="score_goal", player=Pl(1))
    create_event(action="score_goal", player=Pl(1))
    create_event(action="score_goal", player=Pl(3))
    create_event(action="close_set", player=Pl(1))

    response = self.client.get(url)

    # should not raise
    match = response.data
    match["owner"] = self._test1
    match = MatchResultSerializer().create(data=match)
    self.assertIsNotNone(match)
    self.assertNotEqual(response.data["teams"][0]["score"], response.data["teams"][1]["score"])
    # TODO test the other properties