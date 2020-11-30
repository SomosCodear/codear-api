import asyncio
import typing
from django.core.management.base import BaseCommand
from events import models


class Command(BaseCommand):
    help = 'Fetches events from external sources'

    async def _fetch_source_events(
        self,
        community_source: models.CommunityEventSource,
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        source_events: typing.List[typing.Dict[str, typing.Any]] = []

        try:
            self.stdout.write(f'Fetching events from {community_source}...')
            source_events = community_source.fetch_events()
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(source_events)} events from {community_source}'))
        except Exception as error:
            self.stderr.write(self.style.ERROR(f'Error while processing {community_source}: {error}'))

        return source_events

    async def _fetch_all_events(
        self,
        community_sources: typing.List[models.CommunityEventSource],
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        tasks: typing.List[
            typing.Coroutine[typing.Any, typing.Any, typing.List[typing.Dict[str, typing.Any]]]
        ] = []

        for community_source in community_sources:
            tasks.append(self._fetch_source_events(community_source))

        results = await asyncio.gather(*tasks)
        return [event for events in results for event in events]

    def handle(self, *args, **options): # type: ignore
        # get events from sources
        community_sources = list(models.CommunityEventSource.objects.all())
        fetched_events = asyncio.run(self._fetch_all_events(community_sources))

        # create or update eventj
        self.stdout.write(f'Creating/updating {len(fetched_events)} events...')
        created_count = 0
        updated_count = 0

        for event in fetched_events:
            external_reference = event.pop('external_reference')
            _, created = models.Event.objects.update_or_create(
                external_reference=external_reference,
                defaults=event,
            )

            if created:
                created_count += 1
            else:
                updated_count += 1


        self.stdout.write(self.style.SUCCESS(f'Created {created_count} and updated {updated_count} events!'))

