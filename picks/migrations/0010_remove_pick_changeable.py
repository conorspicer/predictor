# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-10 09:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picks', '0009_pick_changeable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pick',
            name='changeable',
        ),
    ]
