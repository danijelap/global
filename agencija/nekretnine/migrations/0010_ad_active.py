# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0009_ad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
