# Generated by Django 3.0.5 on 2020-05-20 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200518_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='trailer',
            name='archivoVideo',
            field=models.FileField(blank=True, null=True, upload_to='static/videos/'),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='archivo',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/'),
        ),
    ]