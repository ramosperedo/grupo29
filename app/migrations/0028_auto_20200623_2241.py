# Generated by Django 3.0.5 on 2020-06-24 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_perfilactual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailer',
            name='titulo',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]