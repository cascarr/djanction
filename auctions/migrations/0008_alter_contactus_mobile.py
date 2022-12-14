# Generated by Django 4.1.1 on 2022-10-08 23:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='mobile',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: "+ 9999999999". Up to 15 digits is allowed.', regex='^\\+\\d{8,15}$')]),
        ),
    ]
