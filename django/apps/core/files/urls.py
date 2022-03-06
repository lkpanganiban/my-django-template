from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import FileSearchViewset, FilesUploadView, FileViewset

router = DefaultRouter()
router.register(r'search', FileSearchViewset, basename='files-search')
router.register(r'', FileViewset, basename='files')

urlpatterns = [
    path('upload/', FilesUploadView.as_view(), name='file-upload'),
]

urlpatterns += router.urls