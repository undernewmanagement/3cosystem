# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0005_auto_20150203_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribution',
            name='comments',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
