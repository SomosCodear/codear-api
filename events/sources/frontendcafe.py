from __future__ import annotations
import typing
import requests
from django.utils import dateparse
from . import base

__all__ = ['FrontendCafeEventSource']


class FrontendCafeEventSource(base.EventSource):
    SOURCE_ID = 'frontend-cafe'
    SOURCE_NAME = 'Frontend Cafe'
    API_URL = 'https://frontend.cafe/api/events'

    def get_new_events(self) -> typing.List[typing.Dict]:
        request = requests.get(self.API_URL)
        result = request.json()
        events: typing.List[typing.Dict] = []

        for fe_event in result:
            event = {
                'name': fe_event['title'],
                'date': dateparse.parse_datetime(fe_event['date']),
                'street': 'Online',
                'city': 'Buenos Aires',
                'link': 'https://frontend.cafe/',
                'external_reference': fe_event['slug'],
            }
            events.append(event)

        return events

    def __str__(self):
        return self.SOURCE_NAME
