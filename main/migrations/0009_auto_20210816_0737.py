# Generated by Django 3.1.7 on 2021-08-16 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='order_number',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.order'),
        ),
    ]
