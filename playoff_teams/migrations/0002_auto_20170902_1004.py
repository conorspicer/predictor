# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-02 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playoff_teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_east',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_east', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_north',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_north', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_south',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_south', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_west',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_west', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_wild1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_wild1', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_wild2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_wild2', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_east',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_east', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_north',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_north', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_south',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_south', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_west',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_west', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_wild1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_wild1', to='fixtures.Team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_wild2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_wild2', to='fixtures.Team'),
        ),
    ]
