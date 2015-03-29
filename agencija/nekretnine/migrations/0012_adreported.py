# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0011_ad_reported_as_inactive_counter'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdReported',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('reporter_token', models.IntegerField()),
                ('reporter_ip_address', models.TextField()),
                ('ad', models.ForeignKey(to='nekretnine.Ad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
