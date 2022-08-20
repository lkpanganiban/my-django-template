# Generated by Django 4.0.2 on 2022-08-20 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_subscriptions_subscriptions_and_more'),
        ('files', '0006_alter_fileset_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileset',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='fileset',
            name='subscription_access',
        ),
        migrations.AddField(
            model_name='fileset',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_set_owner', to='users.subscriptions'),
        ),
    ]