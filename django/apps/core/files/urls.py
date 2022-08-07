from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import FileSearchViewset, FilesUploadView, FileViewset, FileSetViewset

router = DefaultRouter()
router.register(r'api/search', FileSearchViewset, basename='files-search')
router.register(r'api/set', FileSetViewset, basename='set')
router.register(r'api', FileViewset, basename='files')

urlpatterns = [
    path('upload/', FilesUploadView.as_view(), name='file-upload'),
]

urlpatterns += router.urls