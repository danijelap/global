# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0028_auto_20150801_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objekat',
            name='deposit',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
