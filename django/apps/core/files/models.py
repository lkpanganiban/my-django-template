import uuid
from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User, Group


def get_time_now():
    return datetime.now(timezone.utc)


class FileSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = models.JSONField(null=True, blank=True)
    group_access = models.ManyToManyField(Group)

    class Meta:
        verbose_name_plural = "File Sets"
        ordering = ["-create_date"]
        permissions = (
            ("can_merge_sets", "Can merge sets"),
        )

    def __str__(self):
        return str(self.id)


class Files(models.Model):
    """
    list of uploaded files and its metadata.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=999, default="file 1")
    file_type = models.CharField(max_length=999, default="binary")
    file_size = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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

    def get_owner(self):
        return self.owner.email

    def get_file_set(self):
        return str(self.file_set.id)

    def has_group_access(self, group=None):
        return self.file_set.group_access.contains(group)

    def save(self, *args, **kwargs):
        if kwargs.get("force_insert") is not None:  # handle first insert to db
            self.name = self.location.name
            self.file_type = self.location.path.split(".")[-1]
            self.file_size = self.location.size
            new_name = str(self.id) + f".{self.file_type}"
            self.location.name = new_name
        super(Files, self).save(*args, **kwargs)
