# Generated by Django 4.1.3 on 2022-12-24 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_alter_userweekresult_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertotalresult',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
