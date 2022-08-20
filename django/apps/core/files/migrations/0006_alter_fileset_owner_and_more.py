# Generated by Django 4.0.2 on 2022-08-20 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_remove_subscriptions_subscriptions_and_more'),
        ('files', '0005_alter_fileset_subscription_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileset',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_set_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fileset',
            name='subscription_access',
            field=models.ManyToManyField(to='users.Subscriptions'),
        ),
    ]