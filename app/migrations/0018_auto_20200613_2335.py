# Generated by Django 3.0.7 on 2020-06-14 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20200609_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro',
            name='fechaLanzamientoFinal',
        ),
        migrations.AlterField(
            model_name='capitulo',
            name='idLibro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Libro'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/'),
        ),
        migrations.DeleteModel(
            name='Historial',
        ),
    ]
