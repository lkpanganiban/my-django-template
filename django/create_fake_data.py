import os
from random import randint
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

from faker import Faker
from apps.core.files.models import *
from apps.core.users.models import *
from model_bakery.recipe import Recipe, foreign_key
from model_bakery import baker


fake = Faker()

for k in range(20):
    email = fake.email()
    #     user = Recipe(User,
    #                   first_name = fake.first_name,
    #                   last_name = fake.last_name(),
    #                   email = email,
    #                   username= email
    #     )
    user = baker.make(
        User,
        first_name=fake.first_name,
        last_name=fake.last_name(),
        email=email,
        username=email,
    )
    subscription = Subscriptions.objects.get(owner=user)
    file_set = FileSet.objects.create(
        subscription=subscription        
    )
    file_name = fake.file_name()
    location = f"/usr/src/app/files/{file_name}"
    files = Files.objects.create(
        file_set=file_set,
        name = file_name,
        file_size=randint(100,10000),
        description=fake.sentence(),
        file_type=file_name.split(".")[1],
        location=location

    )
