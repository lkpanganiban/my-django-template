from django.dispatch import receiver

from django.db.models.signals import post_save
from .models import FileSet
from .actions import add_moderator_permission_to_moderators


@receiver(post_save, sender=FileSet)
def add_moderator_permission_to_subscription_owner(
    sender, instance=None, created=False, **kwargs
):
    if created:
        instance.moderators.add(instance.subscription.owner)
        add_moderator_permission_to_moderators(instance, instance.subscription.owner)
