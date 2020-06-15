# Generated by Django 3.0.7 on 2020-06-15 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_delete_perfilactual'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilActual',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idPerfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Perfil')),
                ('idSuscriptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
