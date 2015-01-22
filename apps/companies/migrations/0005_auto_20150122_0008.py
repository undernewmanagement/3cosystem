# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_auto_20150106_1612'),
        ('companies', '0004_auto_20150121_0236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='country',
        ),
        migrations.AddField(
            model_name='company',
            name='City',
            field=models.ForeignKey(default=2, to='geography.City'),
            preserve_default=False,
        ),
    ]
