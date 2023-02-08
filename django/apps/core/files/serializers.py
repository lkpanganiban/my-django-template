import os

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .models import Files, FileSet
from .actions import assign_moderator_permissions


class FileSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSet
        fields = "__all__"

    def _add_moderators_to_file_set(self, fs, moderators_list):
        if len(moderators_list) == 0:
            return fs
        for m in moderators_list:
            fs.moderators.add(m.id)
            assign_moderator_permissions(m, fs.id)
        return fs

    def create(self, validated_data):
        moderators_list = validated_data.pop("moderators")
        fs = FileSet.objects.create(**validated_data)
        fs = self._add_moderators_to_file_set(fs, moderators_list)
        return fs

    def update(self, instance, validated_data):
        moderators_list = validated_data.pop("moderators")
        instance.tags = validated_data.get("tags", instance.tags)
        instance.save()
        return self._add_moderators_to_file_set(instance, moderators_list)


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
            "file_set",
        ]


if int(os.environ.get("ELASTICSEARCH", 0)):
    from .documents import FilesDocument

    class FilesDocumentSerializer(DocumentSerializer):
        class Meta:
            document = FilesDocument
            fields = ("id", "name", "file_type", "file_size", "location")
