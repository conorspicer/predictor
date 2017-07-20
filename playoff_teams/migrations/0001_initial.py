# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-16 17:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fixtures', '0010_fixture_changeable'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayoffPick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('afc_east', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='afc_east', to='fixtures.Team')),
                ('afc_north', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='afc_north', to='fixtures.Team')),
                ('afc_south', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='afc_south', to='fixtures.Team')),
                ('afc_west', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='afc_west', to='fixtures.Team')),
                ('afc_wild1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='afc_wild1', to='fixtures.Team')),
                ('afc_wild2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='afc_wild2', to='fixtures.Team')),
                ('nfc_east', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_east', to='fixtures.Team')),
                ('nfc_north', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_north', to='fixtures.Team')),
                ('nfc_south', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_south', to='fixtures.Team')),
                ('nfc_west', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_west', to='fixtures.Team')),
                ('nfc_wild1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_wild1', to='fixtures.Team')),
                ('nfc_wild2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_wild2', to='fixtures.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playoff_pick', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
