# Generated by Django 3.0.2 on 2020-01-24 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20200124_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='_qr_code_data',
        ),
        migrations.AddField(
            model_name='user',
            name='qr_code_data',
            field=models.BinaryField(default=b'No'),
            preserve_default=False,
        ),
    ]
