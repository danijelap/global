# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0007_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='objekat',
            name='owner',
            field=models.ForeignKey(to='nekretnine.Owner', default=1),
            preserve_default=False,
        ),
    ]
