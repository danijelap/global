# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0017_owner_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='objekat',
            name='deposit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objekat',
            name='free_message',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
