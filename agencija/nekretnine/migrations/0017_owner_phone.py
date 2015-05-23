# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nekretnine.models


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0016_auto_20150426_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='phone',
            field=models.BigIntegerField(default=381641234567, validators=[nekretnine.models.validate_positive_number]),
            preserve_default=False,
        ),
    ]
