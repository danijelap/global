# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0026_auto_20150801_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objekat',
            name='deposit',
            field=models.BooleanField(),
            preserve_default=True,
        ),
    ]
