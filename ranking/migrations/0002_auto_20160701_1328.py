# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='ranking',
        ),
        migrations.AddField(
            model_name='team',
            name='mu',
            field=models.FloatField(default=25),
        ),
        migrations.AddField(
            model_name='team',
            name='sigma',
            field=models.FloatField(default=8.333),
        ),
    ]
