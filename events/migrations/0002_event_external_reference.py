# Generated by Django 3.1 on 2020-11-15 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='external_reference',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
