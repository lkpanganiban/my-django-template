from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import RegisterView, UserViewset

router = DefaultRouter()
router.register(r'', UserViewset, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
]
urlpatterns += router.urls