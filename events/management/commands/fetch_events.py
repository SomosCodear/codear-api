import abc
from types import new_class
import requests
from django.core.management.base import BaseCommand, CommandError
from django.utils import dateparse
from events import models


class EventSource(abc.ABC):
  @classmethod
  def get_source_name(cls):
    return cls.SOURCE_NAME

  @classmethod
  @abc.abstractmethod
  def get_new_events(self) -> models.Event:
    pass


class FrontendCafeSource(EventSource):
  SOURCE_NAME = 'Frontend Cafe'
  API_URL = 'https://frontend.cafe/api/events'

  @classmethod
  def get_new_events(cls) -> models.Event:
    request = requests.get(cls.API_URL)
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


class Command(BaseCommand):
    help = 'Fetches events from external sources'

    def handle(self, *args, **options):
      new_events = []

      for source in EventSource.__subclasses__():
        source_name = source.get_source_name()
        self.stdout.write(f'Fetching events from {source_name}...')
        source_events = source.get_new_events()
        self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(source_events)} events from {source_name}'))

        new_events.extend(source_events)

      self.stdout.write(f'Saving {len(new_events)} events...')
      models.Event.objects.bulk_create(new_events)
      self.stdout.write(self.style.SUCCESS('Done!'))



