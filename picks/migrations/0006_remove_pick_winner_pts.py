# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-09 09:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picks', '0005_auto_20170709_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pick',
            name='winner_pts',
        ),
    ]
