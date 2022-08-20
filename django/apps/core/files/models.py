import uuid
from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User
from apps.core.users.models import Subscriptions


def get_time_now():
    return datetime.now(timezone.utc)


class FileSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = models.JSONField(null=True, blank=True)
    subscription = models.ForeignKey(Subscriptions, on_delete=models.CASCADE, null=True, blank=True, related_name="file_set_owner")

    class Meta:
        verbose_name_plural = "File Sets"
        ordering = ["-create_date"]
        permissions = (("can_merge_sets", "Can merge sets"),)

    def __str__(self):
        return str(self.id)

    @property
    def owner_email(self):
        return self.subscription.owner.email
    
    def has_subscription_access(self, subscription=None):
        if subscription.status:
            return self.subscription_access.contains(subscription)
        return False

class Files(models.Model):
    """
    list of uploaded files and its metadata.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=999, default="file 1")
    file_type = models.CharField(max_length=999, default="binary")
    file_size = models.IntegerField(default=0)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    file_set = models.ForeignKey(FileSet, on_delete=models.CASCADE, null=True)
    location = models.FileField(upload_to="files")
    description = models.TextField(null=True, blank=True)
    is_shareable = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Files"
        ordering = ["-create_date"]

    def __str__(self):
        return str(self.id)

    @property
    def owner_email(self):
        return self.file_set.subscription.owner.email

    def has_subscription_access(self, subscription=None):
        if subscription.status:
            return self.file_set.subscription == subscription
        return False

    def save(self, *args, **kwargs):
        if kwargs.get("force_insert") is not None:  # handle first insert to db
            self.name = self.location.name.split("/")[-1]
            try:
                self.file_type = self.location.path.split(".")[-1]
                self.file_size = self.location.size
            except:
                pass
            new_name = str(self.id) + f".{self.file_type}"
            self.location.name = new_name
        super(Files, self).save(*args, **kwargs)
