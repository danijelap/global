# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0027_auto_20150801_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objekat',
            name='construction_year',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
