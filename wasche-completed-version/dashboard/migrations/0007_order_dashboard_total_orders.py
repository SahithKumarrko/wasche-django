# Generated by Django 3.0.2 on 2020-01-23 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_delete_overflown_orders_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_dashboard',
            name='total_orders',
            field=models.CharField(default='0', max_length=254),
        ),
    ]
