from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from trueskill import TrueSkill, Rating


class Rating(models.Model):
  rating_mu = models.FloatField(default=Rating().mu)
  rating_sigma = models.FloatField(default=Rating().sigma)

  class Meta:
    abstract = True

  @property
  def rating(self):
    return self.rating_mu - 1 * self.rating_sigma


class Player(Rating):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  @receiver(post_save, sender=User)
  def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)


class Match(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey("auth.User", related_name="matches", on_delete=models.CASCADE)


class MatchTeam(models.Model):
  index = models.IntegerField()
  score = models.IntegerField()
  match = models.ForeignKey(Match, on_delete=models.CASCADE)

  # TODO store this on the model
  @property
  def winner(self):
    for enemy in self.match.matchteam_set.all():
      if self.score < enemy.score:
        return False
    return True


class MatchPlayer(Rating):
  # store pre-match player ratings
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  team = models.ForeignKey(MatchTeam, on_delete=models.CASCADE)


class MatchTeamSet(models.Model):
  match_team = models.ForeignKey(MatchTeam, on_delete=models.CASCADE)
  index = models.IntegerField()
  points = models.IntegerField()
  color = models.CharField(max_length=255)