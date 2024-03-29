from cProfile import Profile
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import UserViewset, RegisterView, ProfileViewset, SubscriptionViewset
from .views import *

router = DefaultRouter()
router.register(r'api/list', UserViewset, basename='user-list')
router.register(r'api/profile', ProfileViewset, basename='user-profile')
router.register(r'api/subscriptions', SubscriptionViewset, basename='subscriptions')

urlpatterns = [
    path('api/register', RegisterView.as_view(), name='user-register'),
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
    path('register/', register_page, name="register")
]
urlpatterns += router.urls