# Generated by Django 3.0.5 on 2020-05-14 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_libro_ultimo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libro',
            old_name='ultimo',
            new_name='ultimoCapitulo',
        ),
        migrations.AddField(
            model_name='capitulo',
            name='fechaLanzamiento',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='capitulo',
            name='fechaVencimiento',
            field=models.DateField(auto_now=True),
        ),
    ]