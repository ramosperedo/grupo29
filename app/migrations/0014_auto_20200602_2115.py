# Generated by Django 3.0.5 on 2020-06-03 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_capitulo_numero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitulo',
            name='numero',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
