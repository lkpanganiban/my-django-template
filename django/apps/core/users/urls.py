from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import UserViewset, RegisterView
from .views import *

router = DefaultRouter()
router.register(r'api/list', UserViewset, basename='user-list')

urlpatterns = [
    path('api/register', RegisterView.as_view(), name='user-register'),
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
    path('register/', register_page, name="register")
]
urlpatterns += router.urls