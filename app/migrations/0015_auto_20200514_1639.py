# Generated by Django 3.0.5 on 2020-05-14 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_merge_20200512_2332'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='tarjeta',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='tipotarjeta',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='dni',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]