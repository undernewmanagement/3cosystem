# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import location_field.models.spatial


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=50)),
                ('long_name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('distance', models.IntegerField()),
                ('is_active', models.BooleanField(default=False)),
                ('location', location_field.models.spatial.LocationField(default=b'POINT(0.0 0.0)', srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('weight', models.IntegerField()),
                ('region', models.CharField(default=b'NA', max_length=2, choices=[(b'NA', b'North America'), (b'SA', b'South America'), (b'EU', b'Europe'), (b'ME', b'Middle East'), (b'AS', b'Asia'), (b'AU', b'Oceania'), (b'AF', b'Africa')])),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='geography.Country'),
            preserve_default=True,
        ),
    ]
