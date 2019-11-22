from django.db import models
from matchlog.models import Player

class Event(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey("auth.User", related_name="events", on_delete=models.CASCADE)

class Log(models.Model):
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  owner = models.ForeignKey("auth.User", related_name="logs", on_delete=models.CASCADE)
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  action = models.CharField(max_length=255)
  payload = models.TextField(default="")