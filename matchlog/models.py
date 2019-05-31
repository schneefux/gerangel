from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
  user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
  rating_mu = models.FloatField()
  rating_sigma = models.FloatField()


class Match(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  in_progress = models.BooleanField(default=True)
  home_player = models.ForeignKey(
    Player,
    on_delete=models.DO_NOTHING,
    related_name='match_home_set')
  away_player = models.ForeignKey(
    Player,
    on_delete=models.DO_NOTHING,
    related_name='match_away_set')
  home_score = models.IntegerField()
  away_score = models.IntegerField()
