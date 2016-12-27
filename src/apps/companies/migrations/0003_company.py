# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import location_field.models.spatial


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_auto_20150106_1612'),
        ('companies', '0002_auto_20150106_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('slug', models.CharField(max_length=100)),
                ('weight', models.IntegerField(default=0, blank=True)),
                ('website', models.URLField()),
                ('twitter', models.CharField(max_length=50)),
                ('full_address', models.CharField(max_length=200)),
                ('location', location_field.models.spatial.LocationField(default=b'POINT(0.0 0.0)', srid=4326)),
                ('categories', models.ManyToManyField(to='companies.Category')),
                ('country', models.ForeignKey(to='geography.Country')),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
            bases=(models.Model,),
        ),
    ]
