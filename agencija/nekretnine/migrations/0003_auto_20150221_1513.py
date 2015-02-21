# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nekretnine.models


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0002_objectimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='objekat',
            name='floor',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objekat',
            name='floors',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objekat',
            name='has_air_conditioner',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objekat',
            name='has_cable',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objekat',
            name='has_elevator',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objekat',
            name='has_terrace',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='objectimage',
            name='image',
            field=models.ImageField(upload_to=nekretnine.models.ObjectImage.upload_path),
            preserve_default=True,
        ),
    ]
