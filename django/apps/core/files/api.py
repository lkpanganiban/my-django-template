from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets, renderers
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
    OrderingFilterBackend,
    FilteringFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from .models import Files
from .documents import FilesDocument
from .serializers import FilesSerializer, FilesDocumentSerializer


class FilesUploadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        file_serializer = FilesSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Files.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FilesSerializer


class FileSearchViewset(BaseDocumentViewSet):
    document = FilesDocument
    serializer_class = FilesDocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'
    renderer_classes = [renderers.JSONRenderer]

    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
    search_fields = (
        'name',
        'file_type',
        'owner',
    )
    
    ordering_fields = {
        'owner': 'owner.raw',
        'file_type': 'file_type.raw'
    }
    ordering = ('_score',)

    filter_fields = {
        'id': 'id',
        'name': 'name',
        'file_type': 'file_type',
        'owner': 'owner',
        'location': 'location'
    }
