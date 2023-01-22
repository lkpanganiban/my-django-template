import os
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import FilesUploadView, FileViewset, FileSetViewset

router = DefaultRouter()
router.register(r"api/set", FileSetViewset, basename="set")
router.register(r"api", FileViewset, basename="files")

if int(os.environ.get("ELASTICSEARCH",0)):
    from .api import FileSearchViewset
    router.register(r"api/search", FileSearchViewset, basename="files-search")


urlpatterns = [
    path("upload/", FilesUploadView.as_view(), name="file-upload"),
]

urlpatterns += router.urls
