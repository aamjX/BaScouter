# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-15 14:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_auto_20170515_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 15, 16, 42, 17, 43256)),
        ),
    ]
