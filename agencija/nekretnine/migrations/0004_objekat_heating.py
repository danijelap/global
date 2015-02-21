# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0003_auto_20150221_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='objekat',
            name='heating',
            field=models.ForeignKey(to='nekretnine.Heating', default=1),
            preserve_default=False,
        ),
    ]
