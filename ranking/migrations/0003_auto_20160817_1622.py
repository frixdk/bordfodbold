# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-17 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0002_auto_20160701_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='mu',
            field=models.FloatField(default=25),
        ),
        migrations.AddField(
            model_name='player',
            name='sigma',
            field=models.FloatField(default=8.333),
        ),
    ]
