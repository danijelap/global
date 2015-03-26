# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0006_auto_20150221_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('email', models.TextField(validators=[django.core.validators.EmailValidator()])),
                ('phone', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
