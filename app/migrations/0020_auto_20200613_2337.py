# Generated by Django 3.0.7 on 2020-06-14 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_historial_perfilactual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfilactual',
            name='idPerfil',
        ),
        migrations.RemoveField(
            model_name='perfilactual',
            name='idSuscriptor',
        ),
        migrations.DeleteModel(
            name='Historial',
        ),
        migrations.DeleteModel(
            name='PerfilActual',
        ),
    ]
