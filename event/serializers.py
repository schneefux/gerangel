from django.contrib.auth.models import User
from rest_framework import serializers

from event.models import Event, Log

class EventSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source="owner.id")

  class Meta:
    model = Event
    fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source="owner.id")

  class Meta:
    model = Log
    fields = '__all__'
