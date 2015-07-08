# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0022_owner_phone_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='owner',
            old_name='phone_public',
            new_name='show_data_in_ad',
        ),
    ]
