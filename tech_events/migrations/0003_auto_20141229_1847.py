# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tech_events', '0002_auto_20141227_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techevent',
            name='city',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='techevent',
            name='country',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='techevent',
            name='postal_code',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
    ]
