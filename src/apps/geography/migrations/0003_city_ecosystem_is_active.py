# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_auto_20150106_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='ecosystem_is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
