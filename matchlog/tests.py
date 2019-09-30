from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from matchlog.models import Match, Player, User


class MatchTests(APITestCase):
  def setUp(self):
    User.objects.create(username='test1')
    User.objects.create(username='test2')
    User.objects.create(username='test3')
    User.objects.create(username='test4')

  def test_create_match(self):
    url = reverse("matches-results-list")
    data = {
      "home_score": 3,
      "away_score": 2,
      "home_players": [1, 2],
      "away_players": [3, 4],
    }

    response = self.client.post(url, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Match.objects.count(), 1)