# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-15 14:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_auto_20170515_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 15, 16, 43, 53, 272993)),
        ),
    ]
