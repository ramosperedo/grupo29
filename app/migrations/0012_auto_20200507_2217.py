# Generated by Django 3.0.5 on 2020-05-08 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20200507_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='idTarjeta',
            field=models.IntegerField(default=0),
        ),
    ]
