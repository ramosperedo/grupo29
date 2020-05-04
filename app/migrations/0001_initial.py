# Generated by Django 3.0.5 on 2020-05-02 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('maximoPremium', models.IntegerField(default=4)),
                ('maximoStandar', models.IntegerField(default=2)),
                ('Premium', models.IntegerField(default=1)),
                ('Standar', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('autor', models.CharField(max_length=50)),
                ('isbn', models.IntegerField(unique=True)),
                ('genero', models.CharField(max_length=20)),
                ('editorial', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=250)),
                ('foto', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Novedad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=150)),
                ('archivo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('foto', models.CharField(max_length=50)),
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
                ('descripcion', models.CharField(max_length=150)),
                ('archivo', models.CharField(max_length=100)),
                ('idLibro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Libro')),
            ],
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreTitular', models.CharField(max_length=50)),
                ('numero', models.IntegerField()),
                ('clave', models.IntegerField()),
                ('fechaVencimiento', models.IntegerField()),
                ('idTipoTarjeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TipoTarjeta')),
            ],
        ),
        migrations.CreateModel(
            name='Suscriptor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('clave', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('premium', models.IntegerField()),
                ('idTarjeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Tarjeta')),
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
        migrations.AddField(
            model_name='perfil',
            name='idSuscriptor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Suscriptor'),
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
            name='Capitulos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('archivo', models.CharField(max_length=100)),
                ('idLibro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Libro')),
            ],
        ),
    ]