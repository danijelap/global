# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to='objects')),
                ('object', models.ForeignKey(to='nekretnine.Objekat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
