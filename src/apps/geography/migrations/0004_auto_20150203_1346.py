# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0003_city_ecosystem_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(max_length=255)),
                ('comments', models.TextField(max_length=1000, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='attributions',
            field=models.ManyToManyField(to='geography.Attribution'),
            preserve_default=True,
        ),
    ]
