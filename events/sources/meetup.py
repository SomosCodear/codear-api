from __future__ import annotations
import typing
import requests
from django.utils import timezone
from events import models
from . import base

__all__ = ['MeetupEventSource']


class MeetupEventSource(base.EventSource):
  SOURCE_ID = 'meetup'
  SOURCE_NAME = 'Meetup'
  API_URL = 'https://api.meetup.com/{community_id}/events?page=10'

  def __init__(self, community_id=None):
    assert community_id, 'A community id is needed to run a Meetup source'
    self.community_id = community_id

  def get_new_events(self) -> typing.List[models.Event]:
    url = self.API_URL.format(community_id=self.community_id)
    request = requests.get(url)
    result = request.json()
    events = []

    for meetup_event in result:
      event = models.Event(
        name=meetup_event['name'],
        date=timezone.make_aware(timezone.datetime.utcfromtimestamp(meetup_event['time'])),
        street=meetup_event['venue']['name'],
        city=meetup_event['group']['localized_location'],
        link=meetup_event['link'],
        external_reference=meetup_event['id'],
      )
      events.append(event)

    return events

  def __str__(self):
    return f'{self.SOURCE_NAME} ({self.community_id})'

