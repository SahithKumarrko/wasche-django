# Generated by Django 3.0.2 on 2020-01-16 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='image_url',
            field=models.CharField(default='', max_length=254),
        ),
    ]
