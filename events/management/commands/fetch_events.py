import asyncio
import typing
from django.core.management.base import BaseCommand
from events import models


class Command(BaseCommand):
    help = 'Fetches events from external sources'

    async def _fetch_source_events(self, community_source: models.CommunityEventSource) -> typing.List[models.Event]:
        source_events: typing.List[models.Event] = []

        try:
            self.stdout.write(f'Fetching events from {community_source}...')
            source_events = community_source.fetch_events()
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(source_events)} events from {community_source}'))
        except Exception as error:
            self.stderr.write(self.style.ERROR(f'Error while processing {community_source}: {error}'))

        return source_events

    async def _fetch_all_events(self, community_sources: models.CommunityEventSource) -> typing.List[models.Event]:
        tasks: typing.List[typing.Coroutine[typing.Any, typing.Any, typing.List[models.Event]]] = []

        for community_source in community_sources:
            tasks.append(self._fetch_source_events(community_source))

        results = await asyncio.gather(*tasks)
        return [event for events in results for event in events]

    def handle(self, *args, **options):
        # get events from sources
        community_sources = list(models.CommunityEventSource.objects.all())
        fetched_events = asyncio.run(self._fetch_all_events(community_sources))

        # filter out already created events
        existing_event_references = models.Event.objects.filter(
            external_reference__in=[event.external_reference for event in fetched_events],
        ).values_list('external_reference', flat=True)
        new_events = [event for event in fetched_events if event.external_reference not in existing_event_references ]

        self.stdout.write(f'Saving {len(new_events)} events...')
        models.Event.objects.bulk_create(new_events)
        self.stdout.write(self.style.SUCCESS('Done!'))



