# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeoGrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('naziv', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Drzava',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('naziv', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('naziv', models.CharField(max_length=50)),
                ('drzava', models.ForeignKey(to='nekretnine.Drzava')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Namestenost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('naziv', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Objekat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('adresa', models.TextField()),
                ('broj_soba', models.FloatField()),
                ('povrsina', models.IntegerField()),
                ('cena', models.IntegerField()),
                ('deo_grada', models.ForeignKey(to='nekretnine.DeoGrada')),
                ('namestenost', models.ForeignKey(to='nekretnine.Namestenost')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipObjekta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('naziv', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='objekat',
            name='tip_objekta',
            field=models.ForeignKey(to='nekretnine.TipObjekta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deograda',
            name='grad',
            field=models.ForeignKey(to='nekretnine.Grad'),
            preserve_default=True,
        ),
    ]
