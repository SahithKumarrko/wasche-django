# Generated by Django 3.0.2 on 2020-01-30 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracker',
            name='ordered_data',
        ),
        migrations.AddField(
            model_name='tracker',
            name='completion_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 30, 20, 48, 5, 789899), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tracker',
            name='type_op',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='completed_status',
            field=models.CharField(default='', max_length=500),
        ),
    ]
