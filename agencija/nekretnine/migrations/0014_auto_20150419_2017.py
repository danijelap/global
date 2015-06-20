# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nekretnine', '0013_auto_20150329_2133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'ordering': ['-active', '-reported_as_inactive_counter']},
        ),
        migrations.RemoveField(
            model_name='owner',
            name='email',
        ),
        migrations.RemoveField(
            model_name='owner',
            name='name',
        ),
        migrations.AddField(
            model_name='owner',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
    ]
