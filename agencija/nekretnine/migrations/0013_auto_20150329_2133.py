# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0012_adreported'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdReporter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('reporter_token', models.IntegerField()),
                ('reporter_ip_address', models.TextField()),
                ('ad', models.ForeignKey(to='nekretnine.Ad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='adreported',
            name='ad',
        ),
        migrations.DeleteModel(
            name='AdReported',
        ),
    ]
