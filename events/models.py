import json
from django.db import models
from . import sources


class Event(models.Model):
    name = models.CharField(max_length=500)
    date = models.DateTimeField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Argentina')
    link = models.URLField()
    external_reference = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class CommunityEventSource(models.Model):
    SOURCE_CHOICES =[
        (source_id, source.get_source_name())
        for (source_id, source) in sources.all_sources.items()
    ]

    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255, choices=SOURCE_CHOICES)
    params = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} ({self.source})'

    def get_event_source(self) -> sources.EventSource:
        EventSourceClass = sources.all_sources[self.source]

        try:
            params = json.loads(self.params)
        except json.JSONDecodeError:
            params = {}

        return EventSourceClass(**params)
