# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-14 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0006_auto_20170514_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='likes',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
