# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0005_auto_20150221_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deograda',
            old_name='naziv',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='drzava',
            old_name='naziv',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='grad',
            old_name='naziv',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='tipobjekta',
            old_name='naziv',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='objekat',
            name='has_air_conditioner',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='objekat',
            name='has_cable',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='objekat',
            name='has_elevator',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='objekat',
            name='has_terrace',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
