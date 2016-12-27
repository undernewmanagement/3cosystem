# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_auto_20150106_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100)),
                ('weight', models.IntegerField(default=0, blank=True)),
                ('city', models.ManyToManyField(to='geography.City')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
