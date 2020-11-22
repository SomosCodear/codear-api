from __future__ import annotations
import requests
from django.utils import dateparse
from events import models
from . import base

__all__ = ['FrontendCafeEventSource']


class FrontendCafeEventSource(base.EventSource):
  SOURCE_ID = 'frontend-cafe'
  SOURCE_NAME = 'Frontend Cafe'
  API_URL = 'https://frontend.cafe/api/events'

  def get_new_events(self) -> models.Event:
    request = requests.get(self.API_URL)
    result = request.json()
    events = []

    for fe_event in result:
      if models.Event.objects.filter(external_reference=fe_event['slug']).first() is None:
        event = models.Event(
          name=fe_event['title'],
          date=dateparse.parse_datetime(fe_event['date']),
          street='Online',
          city='Buenos Aires',
          link='https://frontend.cafe/',
          external_reference=fe_event['slug'],
        )
        events.append(event)

    return events

