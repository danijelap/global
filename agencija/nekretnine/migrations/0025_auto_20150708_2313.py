# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nekretnine', '0024_usermessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermessage',
            old_name='sender_it_address',
            new_name='sender_ip_address',
        ),
    ]
