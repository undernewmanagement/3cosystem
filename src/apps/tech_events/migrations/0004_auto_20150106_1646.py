# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.tech_events.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tech_events', '0003_auto_20141229_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetupgroup',
            name='url',
            field=models.CharField(unique=True, max_length=100, validators=[apps.tech_events.validators.validate_meetup_url_exists]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='techevent',
            name='meetup_group',
            field=models.ForeignKey(blank=True, to='tech_events.MeetupGroup', null=True),
            preserve_default=True,
        ),
    ]
