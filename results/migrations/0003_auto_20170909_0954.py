# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-09 09:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_auto_20170708_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertotalresult',
            name='total_points_scored',
        ),
        migrations.RemoveField(
            model_name='userweekresult',
            name='user_points',
        ),
    ]
