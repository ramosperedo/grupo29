# Generated by Django 3.0.5 on 2020-07-07 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='idLibro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Libro'),
        ),
    ]