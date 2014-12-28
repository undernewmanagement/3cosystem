# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tech_events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='techevent',
            name='end_time',
        ),
        migrations.AlterField(
            model_name='techevent',
            name='address',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='techevent',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
