# Generated by Django 4.1.3 on 2022-12-24 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fixtures', '0001_initial'),
        ('playoff_teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playoffpick',
            name='afc_wild3',
            field=models.ForeignKey(blank=True, limit_choices_to={'conference': 'AFC'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_wild3', to='fixtures.team'),
        ),
        migrations.AddField(
            model_name='playoffpick',
            name='nfc_wild3',
            field=models.ForeignKey(blank=True, limit_choices_to={'conference': 'NFC'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_wild3', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_east',
            field=models.ForeignKey(blank=True, limit_choices_to={'division': 'AFC_EAST'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_east', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_north',
            field=models.ForeignKey(blank=True, limit_choices_to={'division': 'AFC_NORTH'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_north', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_south',
            field=models.ForeignKey(blank=True, limit_choices_to={'division': 'AFC_SOUTH'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_south', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_west',
            field=models.ForeignKey(blank=True, limit_choices_to={'division': 'AFC_WEST'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_west', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_wild1',
            field=models.ForeignKey(blank=True, limit_choices_to={'conference': 'AFC'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_wild1', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='afc_wild2',
            field=models.ForeignKey(blank=True, limit_choices_to={'conference': 'AFC'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='afc_wild2', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_east',
            field=models.ForeignKey(blank=True, limit_choices_to={'division': 'NFC_EAST'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_east', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_north',
            field=models.ForeignKey(blank=True, limit_choices_to={'division': 'NFC_NORTH'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_north', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_south',
            field=models.ForeignKey(blank=True, limit_choices_to={'division': 'NFC_SOUTH'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_south', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_west',
            field=models.ForeignKey(blank=True, limit_choices_to={'division': 'NFC_WEST'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_west', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_wild1',
            field=models.ForeignKey(blank=True, limit_choices_to={'conference': 'NFC'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_wild1', to='fixtures.team'),
        ),
        migrations.AlterField(
            model_name='playoffpick',
            name='nfc_wild2',
            field=models.ForeignKey(blank=True, limit_choices_to={'conference': 'NFC'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nfc_wild2', to='fixtures.team'),
        ),
    ]
