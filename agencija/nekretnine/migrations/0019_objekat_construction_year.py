# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0018_auto_20150627_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='objekat',
            name='construction_year',
            field=models.IntegerField(default=1970),
            preserve_default=False,
        ),
    ]
