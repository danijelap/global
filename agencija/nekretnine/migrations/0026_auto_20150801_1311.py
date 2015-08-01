# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nekretnine.models


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0025_auto_20150708_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objekat',
            name='additional_features',
            field=models.ManyToManyField(blank=True, to='nekretnine.AdditionalFeatures'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='objekat',
            name='free_message',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='owner',
            name='phone',
            field=models.BigIntegerField(null=True, validators=[nekretnine.models.validate_positive_number]),
            preserve_default=True,
        ),
    ]
