# Generated by Django 4.0.2 on 2022-08-27 01:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_account_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_expiry',
            field=models.DateTimeField(default=datetime.datetime(2032, 7, 5, 1, 33, 52, 423111, tzinfo=utc)),
        ),
    ]
