# Generated by Django 4.0.2 on 2022-02-27 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='file 1', max_length=999)),
                ('file_type', models.CharField(default='binary', max_length=999)),
                ('file_size', models.IntegerField(default=0)),
                ('location', models.FileField(upload_to='files')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_shareable', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Files',
                'ordering': ['-create_date'],
            },
        ),
    ]
