# Generated by Django 2.2 on 2021-08-14 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_drink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drink',
            name='content_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drinks_created', to='main.User'),
        ),
    ]
