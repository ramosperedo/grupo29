# Generated by Django 3.0.5 on 2020-05-17 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200517_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novedad',
            name='descripcion',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='descripcion',
            field=models.CharField(max_length=1000),
        ),
    ]
