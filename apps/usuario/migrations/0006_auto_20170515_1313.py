# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-15 11:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_auto_20170515_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 15, 13, 13, 35, 628378)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
