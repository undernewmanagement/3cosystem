# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import location_field.models.spatial
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeetupGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('is_blacklisted', models.BooleanField(default=False)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
            ],
            options={
                'verbose_name_plural': 'Meetup Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParseError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateField()),
                ('error_message', models.TextField()),
                ('payload', models.TextField()),
                ('is_resolved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Firehose Parse Errors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TechEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uniqid', models.CharField(unique=True, max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('begin_time', models.DateTimeField(verbose_name=b'begin time')),
                ('end_time', models.DateTimeField(verbose_name=b'end time')),
                ('source', models.CharField(default=b'CU', max_length=2, choices=[(b'MU', b'Meetup.com'), (b'EB', b'EventBrite'), (b'IC', b'.ics calendar'), (b'CU', b'Custom one-off event')])),
                ('is_active', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=50)),
                ('location', location_field.models.spatial.LocationField(default=b'POINT (0.0 0.0)', srid=4326)),
                ('meetup_group', models.ForeignKey(to='tech_events.MeetupGroup', null=True)),
            ],
            options={
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
    ]
