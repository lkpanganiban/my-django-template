import os 
from random import randint
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")

import django 
django.setup() 

from faker import factory,Faker 
from apps.core.files.models import * 
from apps.core.users.models import *
from django.contrib.auth.models import Group
from model_bakery.recipe import Recipe,foreign_key

fake = Faker() 

for k in range(20):
    try:
        first_name, last_name = fake.name().split(" ")
    except:
        continue
    email = fake.email()
    user = Recipe(User,
                  first_name = first_name,
                  last_name = last_name,
                  email = email,
                  username= email
    )
    file_set = Recipe(FileSet,
            owner=foreign_key(user)
    )
    filename = fake.company()
    files = Recipe(Files,
            name=filename,
            file_set=foreign_key(file_set),
            file_size=randint(100,2000),
            description=fake.sentence(),
            file_type="pdf",
            location=fake.sentence()
    )
    files.make()