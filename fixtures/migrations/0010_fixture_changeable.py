# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-09 18:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixtures', '0009_auto_20170702_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='changeable',
            field=models.BooleanField(default=True),
        ),
    ]
