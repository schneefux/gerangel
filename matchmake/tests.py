from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from matchlog.models import User


class MatchMakeTests(APITestCase):
  def setUp(self):
    User.objects.create_user(username="test1", password="test1")
    User.objects.create_user(username="test2", password="test2")
    User.objects.create_user(username="test3", password="test3")
    User.objects.create_user(username="test4", password="test4")

  def test_should_matchmake(self):
    url = reverse("matchmake-list")

    response = self.client.get(url + "?id=1&id=2&id=3&id=4")

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.data["results"]
    self.assertEqual(len(data), 21)
    self.assertGreater(data[0]["quality"], data[-1]["quality"])
    self.assertGreater(data[0]["win_probability"][0], data[0]["win_probability"][1])