# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0004_auto_20150203_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='attributions',
        ),
        migrations.AddField(
            model_name='attribution',
            name='city',
            field=models.ForeignKey(related_name='attributions', default=1, to='geography.City'),
            preserve_default=False,
        ),
    ]
