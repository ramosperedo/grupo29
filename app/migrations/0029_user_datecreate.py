# Generated by Django 3.0.5 on 2020-06-28 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20200623_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dateCreate',
            field=models.DateField(auto_now=True),
        ),
    ]