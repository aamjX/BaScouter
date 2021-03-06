# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-14 18:04
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0002_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(null=True, validators=[django.core.validators.URLValidator()])),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('fullName', models.CharField(blank=True, max_length=100, null=True)),
                ('number', models.IntegerField(null=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('flag', models.URLField(null=True, validators=[django.core.validators.URLValidator()])),
                ('birthDate', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(null=True)),
                ('birthPlace', models.CharField(blank=True, max_length=150, null=True)),
                ('value', models.FloatField(null=True)),
                ('position', models.CharField(blank=True, max_length=50, null=True)),
                ('height', models.FloatField(null=True)),
                ('foot', models.CharField(blank=True, max_length=50, null=True)),
                ('contractUntil', models.DateField(null=True)),
                ('inTheTeamSince', models.DateField(null=True)),
                ('agent', models.CharField(blank=True, max_length=150, null=True)),
                ('outfitter', models.CharField(max_length=100, null=True)),
                ('rating', models.FloatField(null=True)),
                ('likes', models.IntegerField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scout.Team')),
            ],
        ),
    ]
