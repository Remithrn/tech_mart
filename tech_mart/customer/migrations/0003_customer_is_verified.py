# Generated by Django 5.0.1 on 2024-02-09 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customer_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
