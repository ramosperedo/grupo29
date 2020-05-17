# Generated by Django 3.0.5 on 2020-05-17 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('superuser', models.BooleanField(default=False)),
                ('idTarjeta', models.IntegerField(default=0)),
                ('premium', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('maximoPremium', models.IntegerField(default=4)),
                ('maximoStandar', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('isbn', models.IntegerField()),
                ('descripcion', models.CharField(max_length=1000)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('vistos', models.IntegerField(default=0, null=True)),
                ('ultimoCapitulo', models.BooleanField(default=False)),
                ('idAutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Autor')),
                ('idEditorial', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Editorial')),
                ('idGenero', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Genero')),
            ],
        ),
        migrations.CreateModel(
            name='Novedad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.CharField(max_length=1000)),
                ('archivo', models.ImageField(blank=True, null=True, upload_to='static/images/')),
                ('archivoVideo', models.FileField(blank=True, null=True, upload_to='static/videos/')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('foto', models.CharField(max_length=50)),
                ('idSuscriptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dni', models.IntegerField(default=0, unique=True)),
                ('numero', models.IntegerField(default=0)),
                ('clave', models.IntegerField(default=0)),
                ('fechaVencimiento', models.DateField()),
                ('tipo', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TipoTarjeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=1000)),
                ('archivo', models.CharField(max_length=100)),
                ('idLibro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Libro')),
            ],
        ),
        migrations.CreateModel(
            name='Recomendaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idLibro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Libro')),
                ('idPerfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idLibro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Libro')),
                ('idPerfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idLibro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Libro')),
                ('idPerfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Capitulo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('archivo', models.CharField(max_length=100)),
                ('fechaLanzamiento', models.DateField(auto_now=True)),
                ('fechaVencimiento', models.DateField(auto_now=True)),
                ('idLibro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Libro')),
            ],
        ),
    ]
