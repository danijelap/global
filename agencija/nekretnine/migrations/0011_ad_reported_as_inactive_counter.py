# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0010_ad_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='reported_as_inactive_counter',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
