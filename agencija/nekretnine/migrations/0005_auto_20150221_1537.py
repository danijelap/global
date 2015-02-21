# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0004_objekat_heating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='namestenost',
            old_name='naziv',
            new_name='name',
        ),
    ]
