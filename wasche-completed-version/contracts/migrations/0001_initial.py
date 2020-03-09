# Generated by Django 2.2.2 on 2019-12-20 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('contract_name', models.CharField(max_length=254, primary_key=True, serialize=False, unique=True)),
                ('contract_address', models.CharField(max_length=254)),
                ('contract_phone_number', models.CharField(max_length=20)),
                ('contract_zip_code', models.CharField(max_length=15)),
                ('contract_country', models.CharField(max_length=100)),
                ('contract_state', models.CharField(max_length=100)),
                ('contract_established_date', models.DateTimeField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'Contracts',
            },
        ),
    ]