# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-09 09:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picks', '0006_remove_pick_winner_pts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pick',
            name='margin_pts',
        ),
        migrations.RemoveField(
            model_name='pick',
            name='totalpts_pts',
        ),
    ]
