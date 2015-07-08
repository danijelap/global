# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0019_objekat_construction_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='objekat',
            name='has_air_conditioner',
        ),
        migrations.RemoveField(
            model_name='objekat',
            name='has_cable',
        ),
        migrations.RemoveField(
            model_name='objekat',
            name='has_elevator',
        ),
        migrations.RemoveField(
            model_name='objekat',
            name='has_terrace',
        ),
        migrations.AddField(
            model_name='objekat',
            name='additional_features',
            field=models.ManyToManyField(to='nekretnine.AdditionalFeatures'),
            preserve_default=True,
        ),
    ]
