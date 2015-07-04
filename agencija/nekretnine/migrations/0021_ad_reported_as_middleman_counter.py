# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0020_auto_20150628_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='reported_as_middleman_counter',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
