# Generated by Django 3.0.5 on 2020-05-07 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200507_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarjeta',
            name='clave',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='fechaVencimiento',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='numero',
            field=models.IntegerField(default=None),
        ),
    ]
