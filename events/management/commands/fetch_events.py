from django.core.management.base import BaseCommand
from events import models


class Command(BaseCommand):
    help = 'Fetches events from external sources'

    def handle(self, *args, **options):
      new_events = []

      community_source: models.CommunityEventSource
      for community_source in models.CommunityEventSource.objects.all():
        source = community_source.get_event_source()

        source_name = source.get_source_name()
        self.stdout.write(f'Fetching events from {source_name}...')
        source_events = source.get_new_events()
        self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(source_events)} events from {source_name}'))

        new_events.extend(source_events)

      self.stdout.write(f'Saving {len(new_events)} events...')
      models.Event.objects.bulk_create(new_events)
      self.stdout.write(self.style.SUCCESS('Done!'))



