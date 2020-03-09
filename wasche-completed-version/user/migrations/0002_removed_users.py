# Generated by Django 2.2.2 on 2019-12-20 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Removed_Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('date_removed', models.DateTimeField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'Removed Users',
            },
        ),
    ]