from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets
from .models import Files
from .serializers import FilesSerializer


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