from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import FilesUploadView, FileViewset

router = DefaultRouter()
router.register(r'', FileViewset, basename='user')

urlpatterns = [
    path('upload/', FilesUploadView.as_view(), name='file-upload'),
]

urlpatterns += router.urls