# Generated by Django 3.0.7 on 2020-06-14 02:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20200613_2337'),
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
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('terminado', models.BooleanField(default=False)),
                ('idCapitulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Capitulo')),
                ('idPerfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Perfil')),
            ],
        ),
    ]
