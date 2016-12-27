# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0003_city_ecosystem_is_active'),
        ('companies', '0006_auto_20150122_0125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='city',
        ),
        migrations.AddField(
            model_name='company',
            name='cites',
            field=models.ManyToManyField(to='geography.City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
