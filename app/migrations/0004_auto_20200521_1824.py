# Generated by Django 3.0.5 on 2020-05-21 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200520_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailer',
            name='idLibro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Libro'),
        ),
    ]
