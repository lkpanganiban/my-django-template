from django.contrib import admin
from .models import Files


class FilesAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'file_type','file_size', 'owner',)
    list_filter = ('file_type',)

    @staticmethod
    def owner(obj):
        return obj.email


admin.site.register(Files, FilesAdmin)