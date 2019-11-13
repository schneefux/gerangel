from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from matchlog.models import Match, Player, User, MatchSetTeam


class MatchTests(APITestCase):
  def setUp(self):
    User.objects.create_user(username="test1", password="test1")
    User.objects.create_user(username="test2", password="test2")
    User.objects.create_user(username="test3", password="test3")
    User.objects.create_user(username="test4", password="test4")

  def _login(self):
    return self.client.login(username="test1", password="test1")

  def _create_match(self):
    url = reverse("matches-results-list")
    data = {
      "home_score": 3,
      "away_score": 2,
      "home_players": [1, 2],
      "away_players": [3, 4],
    }
    return self.client.post(url, data, format="json")

  def _create_match_with_sets(self):
    url = reverse("matches-results-list")
    # TODO normalize data model
    data = {
      "home_score": 2,
      "away_score": 0,
      "home_players": [1, 2],
      "away_players": [3, 4],
      "sets": [{
        "home_color": "red",
        "away_color": "blue",
        "home_points": 8,
        "away_points": 1,
        "home_positions": ["attack", "defense"],
        "away_positions": ["attack", "defense"],
      }, {
        "home_color": "blue",
        "away_color": "red",
        "home_points": 1,
        "away_points": 8,
        "home_positions": ["defense", "attack"],
        "away_positions": ["defense", "attack"],
      }]
    }
    return self.client.post(url, data, format="json")

  def test_should_login(self):
    is_logged_in = self._login()
    self.assertTrue(is_logged_in)

  def test_should_register(self):
    url = reverse("user-list")

    data = {
      "username": "foo",
      "password": "bar",
    }
    response = self.client.post(url, data, format="json")

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_should_register_and_login(self):
    url = reverse("user-list")
    data = {
      "username": "foo",
      "password": "bar",
    }
    self.client.post(url, data, format="json")

    url = reverse("login")
    response = self.client.post(url, data)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("token", response.data)

  def test_should_allow_guest_read_matches(self):
    url = reverse("matches-results-list")
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_should_deny_guest_create_match(self):
    response = self._create_match()
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_should_allow_user_create_match(self):
    self._login()

    response = self._create_match()

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Match.objects.count(), 1)

  def test_should_allow_delete_own_recent_match(self):
    self._login()
    match = self._create_match().data
    url = reverse("matches-results-detail", args=[match["id"]])

    response = self.client.delete(url)

    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Match.objects.count(), 0)

  def test_should_deny_delete_foreign_recent_match(self):
    self._login()
    match = self._create_match().data
    url = reverse("matches-results-detail", args=[match["id"]])
    self.client.login(username="test2", password="test2")

    response = self.client.delete(url)

    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_should_deny_delete_own_old_match(self):
    self._login()
    match = self._create_match().data
    self._create_match()
    url = reverse("matches-results-detail", args=[match["id"]])

    response = self.client.delete(url)

    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_should_filter_players(self):
    url = reverse("player-list")

    response = self.client.get(url + "?user.id=1")

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data["results"]), 1)

  def test_should_matchmake(self):
    # enter a match so that there is a variety of different ratings
    self._login()
    self._create_match()
    url = reverse("player-list")

    response = self.client.get(url + "matchmake/?id=1&id=2&id=3&id=4")

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.data["results"]
    self.assertEqual(len(data), 21)
    self.assertGreater(data[0]["quality"], data[-1]["quality"])
    self.assertGreater(data[0]["win_probability"][0], data[0]["win_probability"][1])

  def test_should_list_match_players(self):
    self._login()
    self._create_match()
    url = reverse("match-players-list")

    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data["results"]), 4)

  def test_should_filter_match_players_by_user_id(self):
    self._login()
    self._create_match()
    self.client.login(username="test2", password="test2")
    self._create_match()
    url = reverse("match-players-list")

    response = self.client.get(url + "?player.user.id=1")

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data["results"]), 2)

  def test_should_add_set_to_match(self):
    self._login()

    response = self._create_match_with_sets()

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(MatchSetTeam.objects.count(), 4)
    self.assertEqual(len(response.data["sets"]), 2)

  def test_should_aggregate_player_stats(self):
    self._login()
    self._create_match_with_sets()
    url = reverse("player-list")

    response = self.client.get(url + "1/stats/")

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["count"], 1)
    self.assertEqual(response.data["sets"], 2)
    self.assertEqual(response.data["wins"], 1)
    self.assertEqual(response.data["points"], 9)