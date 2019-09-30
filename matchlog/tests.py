from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from matchlog.models import Match, Player, User


class MatchTests(APITestCase):
  def setUp(self):
    user1 = User.objects.create(username='test1')
    Player.objects.create(user=user1)
    user2 = User.objects.create(username='test2')
    Player.objects.create(user=user2)
    user3 = User.objects.create(username='test3')
    Player.objects.create(user=user3)
    user4 = User.objects.create(username='test4')
    Player.objects.create(user=user4)

  def test_create_match(self):
    url = reverse("match-list")
    data = {
      "home_score": 3,
      "away_score": 2,
      "home_players": [1, 2],
      "away_players": [3, 4],
    }

    response = self.client.post(url, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Match.objects.count(), 1)