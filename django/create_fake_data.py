import os 
from random import randint
import django 

from faker import Faker
from apps.core.files.models import * 
from apps.core.users.models import *
from model_bakery.recipe import Recipe,foreign_key

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup() 


fake = Faker() 

for k in range(20):
    email = fake.email()
    user = Recipe(User,
                  first_name = fake.first_name,
                  last_name = fake.last_name(),
                  email = email,
                  username= email
    )
    file_set = Recipe(FileSet,
            owner=foreign_key(user)
    )
    filename = fake.file_name()
    files = Recipe(Files,
            name=filename,
            file_set=foreign_key(file_set),
            file_size=randint(100,10000),
            description=fake.sentence(),
            file_type=filename.split(".")[1],
            location=fake.file_path
    )
    files.make()