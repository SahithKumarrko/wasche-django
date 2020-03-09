# Generated by Django 3.0.2 on 2020-03-09 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(default='No Name Provided', max_length=254)),
                ('customer_phone_number', models.CharField(default='', max_length=20)),
                ('plan', models.CharField(default='', max_length=50)),
                ('amount', models.CharField(default='', max_length=10)),
                ('referenceId', models.CharField(default='', max_length=260)),
                ('completed_status', models.BooleanField(default=False)),
                ('eligibility', models.CharField(default='', max_length=400)),
                ('transaction_date', models.DateTimeField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'Transaction Details',
            },
        ),
    ]
