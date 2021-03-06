from __future__ import annotations
import typing
import requests
from django.utils import dateparse, timezone
from . import base

__all__ = ['FrontendCafeEventSource']


class FrontendCafeEventSource(base.EventSource):
    SOURCE_ID = 'frontend-cafe'
    SOURCE_NAME = 'Frontend Cafe'
    API_URL = 'https://frontend.cafe/api/events'

    def get_new_events(self) -> typing.List[typing.Dict[str, typing.Any]]:
        request = requests.get(self.API_URL) # type: ignore
        result: typing.List[typing.Dict[str, typing.Any]] = request.json() # type: ignore
        events: typing.List[typing.Dict[str, typing.Any]] = []

        for fe_event in result:
            event_date = dateparse.parse_datetime(fe_event['date'])

            if event_date is not None and event_date > timezone.now():
                event = {
                    'name': fe_event['title'],
                    'date': event_date,
                    'street': 'Online',
                    'city': 'Buenos Aires',
                    'link': 'https://frontend.cafe/',
                    'external_reference': fe_event['slug'],
                }
                events.append(event)

        return events

    def __str__(self):
        return self.SOURCE_NAME
