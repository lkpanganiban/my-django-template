from ast import Subscript
from rest_framework import status, permissions, viewsets, renderers
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
    OrderingFilterBackend,
    FilteringFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework_tracking.mixins import LoggingMixin
from apps.core.users.models import Subscriptions
from .models import Files, FileSet
from .documents import FilesDocument
from .serializers import FilesSerializer, FilesDocumentSerializer, FileSetSerializer
from .actions import assign_moderator_permissions, merge_sets, assign_moderator_permissions


class FileSetViewset(LoggingMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions of Projects
    """

    queryset = FileSet.objects.all()
    serializer_class = FileSetSerializer
    filterset_fields = ["id"]
    permission_classes = (permissions.IsAuthenticated,)

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    @action(methods=["POST"], detail=False, url_path="merge", url_name="set-merge")
    def merge_file_sets(self, request, **kwargs):
        # assumes that the first item will be the main file set
        set_list = request.data.get("set_list").split(",")
        detail = merge_sets(set_list)
        message = {"detail": detail}
        return Response(message, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="assign-moderator", url_name="assign-moderator")
    def assign_moderator_to_file_set(self, request, **kwargs):
        fs_id = request.data.get("fs_id")
        detail = assign_moderator_permissions(self.request.user, fs_id)
        message = {"detail": detail}
        return Response(message, status=status.HTTP_200_OK)

    def get_queryset(self):
        qs = self.queryset
        if self.request.user.is_superuser:
            return qs
        else:
            request_user_group = self.request.user.user_subscriptions.all().filter(status=True)
            return qs.filter(subscription__in=request_user_group)

    def destroy(self, request, *args, **kwargs):
        qs_object = self.queryset
        qs_id = self.kwargs["pk"]
        sub = Subscriptions.objects.get(owner=self.request.user)
        fileset_object = qs_object.filter(id=qs_id, subscription=sub)
        fileset_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FilesUploadView(LoggingMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_class = (FileUploadParser,)
    decode_request_body = False

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    def post(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        file_serializer = FilesSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileViewset(LoggingMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Files.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FilesSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    def get_queryset(self):
        qs = self.queryset
        if self.request.user.is_superuser:
            return qs
        else:
            request_user_group = self.request.user.user_subscriptions.all().filter(status=True)
            return qs.filter(file_set__subscription__in=request_user_group)


class FileSearchViewset(LoggingMixin, BaseDocumentViewSet):
    document = FilesDocument
    serializer_class = FilesDocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"
    renderer_classes = [renderers.JSONRenderer]

    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
    search_fields = ("name", "file_type", "owner", "description")

    ordering_fields = {"owner": "owner.raw", "file_type": "file_type.raw"}
    ordering = ("_score",)

    filter_fields = {
        "id": "id",
        "name": "name",
        "file_type": "file_type",
        "owner": "owner",
        "location": "location",
        "file_set": "file_set",
    }
    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400
