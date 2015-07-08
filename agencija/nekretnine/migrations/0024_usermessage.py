# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0023_auto_20150704_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('message', models.TextField()),
                ('sender_token', models.IntegerField()),
                ('sender_it_address', models.TextField()),
                ('object', models.ForeignKey(to='nekretnine.Objekat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
