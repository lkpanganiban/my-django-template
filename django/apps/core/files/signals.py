import time
from django.dispatch import receiver

from django.db.models.signals import post_save
from .models import FileSet, Files

# @receiver(post_save, sender=FileSet)
# def add_moderator_permission_to_user(sender, instance=None, created=False, **kwargs):
#     for u in instance.moderators.all():
#         print("yo", assign_moderator_permissions(u, str(instance.id)))