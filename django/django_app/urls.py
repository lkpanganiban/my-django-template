"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.core.users.views import login_page, user_dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("users/", include("apps.core.users.urls")),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("files/", include("apps.core.files.urls")),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("dashboard/", user_dashboard, name="user_dashboard"),
    path("", login_page, name="home"),  # new
]

if int(os.environ.get("PROMETHEUS",0)):
    urlpatterns += [path("stats/", include("django_prometheus.urls"))]


if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static.static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS
    )
