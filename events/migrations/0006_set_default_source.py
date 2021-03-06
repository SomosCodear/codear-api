# Generated by Django 3.1 on 2020-11-22 18:34

from django.db import migrations


def set_default_source(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    CommunityEventSource = apps.get_model('events', 'CommunityEventSource')
    [default_source, created] = CommunityEventSource.objects.get_or_create(
        name='Frontend Cafe',
        source='frontend-cafe',
    )

    changed_events = []
    for event in Event.objects.filter(external_reference__isnull=False):
        event.source = default_source
        changed_events.append(event)

    Event.objects.bulk_update(changed_events, ['source'])


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_source'),
    ]

    operations = [
        migrations.RunPython(set_default_source, migrations.RunPython.noop),
    ]
