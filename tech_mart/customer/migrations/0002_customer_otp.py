# Generated by Django 5.0.1 on 2024-02-09 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='otp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]