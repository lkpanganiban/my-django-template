import uuid
from datetime import datetime, timedelta, timezone
from django.db import models
from django.contrib.auth.models import User


def get_time_now():
    return datetime.now(timezone.utc)



class Files(models.Model):
    '''
    expand this table to add more info for the user like address, job, role, etc.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=999, default="file 1")
    file_type = models.CharField(max_length=999, default="binary")
    file_size = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.FileField(upload_to='files')
    description = models.TextField(null=True, blank=True)
    is_shareable = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Files"
        ordering = ['-create_date']

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        print(self.location)
        self.file_type = self.location.path.split('.')[-1]
        self.file_size = self.location.size
        super(Files, self).save(*args, **kwargs)

