# Generated by Django 3.0.2 on 2020-01-30 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_remove_notifications__qr_code_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onesignal',
            old_name='type',
            new_name='type_os',
        ),
    ]
