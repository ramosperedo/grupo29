# Generated by Django 3.0.5 on 2020-05-07 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200507_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarjeta',
            name='clave',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='dni',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='fechaVencimiento',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='numero',
            field=models.IntegerField(default=0),
        ),
    ]
