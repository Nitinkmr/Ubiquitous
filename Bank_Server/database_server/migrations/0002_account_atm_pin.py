# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-16 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='atm_pin',
            field=models.CharField(default=1110, max_length=4),
        ),
    ]