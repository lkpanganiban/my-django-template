from xml.dom.minidom import Document
from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .models import Files
from .documents import FilesDocument


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = "__all__"

    def get_validation_exclusions(self):
        exclusions = super(FilesSerializer, self).get_validation_exclusions()
        return exclusions + [
            "name",
            "file_type",
            "file_size",
            "description",
            "is_shareable",
            "create_date",
            "update_date",
        ]

class FilesDocumentSerializer(DocumentSerializer):
    class Meta:
        document = FilesDocument
        fields = (
            'id',
            'name',
            'file_type',
            'file_size',
            'location'
        )