# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_auto_20150122_0335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='cites',
            new_name='cities',
        ),
    ]
