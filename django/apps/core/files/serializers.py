from rest_framework import serializers
from .models import Files


class FilesSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(required=False)
    # file_type = serializers.CharField(required=False)
    # file_size = serializers.IntegerField(required=False)
    # owner = serializers.CharField(required=False)
    # description = serializers.TextField(required=False)
    # is_shareable = serializers.BooleanField(required=False)

    class Meta:
        model = Files
        fields = '__all__'

    def get_validation_exclusions(self):
        exclusions = super(FilesSerializer, self).get_validation_exclusions()
        return exclusions + ['name', 'file_type', 'file_size', 'description', 'is_shareable', 'create_date', 'update_date']