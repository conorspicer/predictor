# Generated by Django 4.1.3 on 2022-12-24 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_alter_usertotalresult_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertotalresult',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
