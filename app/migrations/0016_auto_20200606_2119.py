# Generated by Django 3.0.5 on 2020-06-07 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200604_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='foto',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
