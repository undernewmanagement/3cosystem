# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0006_auto_20150203_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='hashtags',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
