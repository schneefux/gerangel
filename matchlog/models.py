from django.db import models
from django.contrib.auth.models import User
from trueskill import TrueSkill, Rating

class Player(models.Model):
  user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
  rating_mu = models.FloatField(default=Rating().mu)
  rating_sigma = models.FloatField(default=Rating().sigma)


class Match(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  in_progress = models.BooleanField(default=True)
  home_players = models.ManyToManyField(
    Player,
    related_name='match_home_set')
  away_players = models.ManyToManyField(
    Player,
    related_name='match_away_set')
  home_score = models.IntegerField()
  away_score = models.IntegerField()
