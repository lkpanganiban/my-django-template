from django.dispatch import receiver

from django.db.models.signals import post_save
from .models import FileSet, Files

@receiver(post_save, sender=FileSet)
def add_owner_to_fileset_group(sender, instance=None, created=False, **kwargs):
    if created:
        instance.subscription_access.add(*instance.owner.subscriptions.all())


@receiver(post_save, sender=Files)
def add_owner_to_files_group(sender, instance=None, created=False, **kwargs):
    if created:
        instance.owner = instance.file_set.owner
        instance.save()