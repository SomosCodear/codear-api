from rest_framework import serializers
from . import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = (
            'name', 'date', 'street', 'city', 'country', 'link',
        )
