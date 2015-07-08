# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0021_ad_reported_as_middleman_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='phone_public',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
