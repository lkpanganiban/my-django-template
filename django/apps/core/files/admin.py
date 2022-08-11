from django.contrib import admin
from .models import FileSet, Files


class FilesAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'file_type','file_size', 'owner','create_date', 'update_date')
    list_filter = ('file_type',)

    @staticmethod
    def owner(obj):
        return obj.email


class FileSetAdmin(admin.ModelAdmin):
    list_display = ('id','owner','create_date', 'update_date')

    @staticmethod
    def owner(obj):
        return obj.email

admin.site.register(Files, FilesAdmin)
admin.site.register(FileSet, FileSetAdmin)