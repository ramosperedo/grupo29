# Generated by Django 3.0.5 on 2020-05-28 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200528_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitulo',
            name='idLibro',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.Libro'),
        ),
    ]
