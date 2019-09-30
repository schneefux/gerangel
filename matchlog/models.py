from django.db import models
from django.contrib.auth.models import User
from trueskill import TrueSkill, Rating


class Rating(models.Model):
  rating_mu = models.FloatField(default=Rating().mu)
  rating_sigma = models.FloatField(default=Rating().sigma)

  class Meta:
    abstract = True


class Player(Rating):
  user = models.OneToOneField(User, on_delete=models.CASCADE)


class Match(models.Model):
  created = models.DateTimeField(auto_now_add=True)


class MatchTeam(models.Model):
  index = models.IntegerField()
  score = models.IntegerField()
  match = models.ForeignKey(Match, on_delete=models.CASCADE)


class MatchPlayer(Rating):
  # store pre-match player ratings
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  team = models.ForeignKey(MatchTeam, on_delete=models.CASCADE)
