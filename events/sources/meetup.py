from __future__ import annotations
import typing
import requests
from django.utils import timezone
from . import base

__all__ = ['MeetupEventSource']


class MeetupEventSource(base.EventSource):
  SOURCE_ID = 'meetup'
  SOURCE_NAME = 'Meetup'
  API_URL = 'https://api.meetup.com/{community_id}/events?page=10'

  def __init__(self, community_id: typing.Optional[str]=None):
    assert community_id, 'A community id is needed to run a Meetup source'
    self.community_id = community_id

  def get_new_events(self) -> typing.List[typing.Dict[str, typing.Any]]:
    url = self.API_URL.format(community_id=self.community_id)
    request = requests.get(url) # type: ignore
    result: typing.List[typing.Dict[str, typing.Any]] = request.json() # type: ignore
    events: typing.List[typing.Dict[str, typing.Any]] = []

    for meetup_event in result:
      event = {
        'name': meetup_event['name'],
        'date': timezone.make_aware(timezone.datetime.utcfromtimestamp(meetup_event['time'])),
        'street': meetup_event['venue']['name'],
        'city': meetup_event['group']['localized_location'],
        'link': meetup_event['link'],
        'external_reference': meetup_event['id'],
      }
      events.append(event)

    return events
