"""
Django settings for django_app project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from distutils import util
from pathlib import Path
from pickle import FALSE

from .log_formatter import CustomisedJSONFormatter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "mysecret-key-1234")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", 1))
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1 [::1] *"
).split(" ")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_json_api",
    "rest_framework.authtoken",
    "rest_framework_tracking",
    "oauth2_provider",
    "corsheaders",
    "guardian",
    "django_browser_reload",
]

# ELASTICSEARCH
if int(os.environ.get("ELASTICSEARCH", 0)):
    INSTALLED_APPS += [
        "django_elasticsearch_dsl",
        "django_elasticsearch_dsl_drf",
    ]
    ELASTICSEARCH_DSL = {
        "default": {"hosts": os.environ.get("ELASTICSEARCH_URL", "localhost:9200")},
    }

if int(os.environ.get("PROMETHEUS", 0)):
    INSTALLED_APPS += ["django_prometheus"]
    PROMETHEUS_BEFORE_MIDDLEWARE = [
        "django_prometheus.middleware.PrometheusBeforeMiddleware"
    ]
    PROMETHEUS_AFTER_MIDDLEWARE = [
        "django_prometheus.middleware.PrometheusAfterMiddleware",
    ]


CORE_APPS = [
    "apps.core.users",
    "apps.core.files",
]

PLUGIN_APPS = []
CUSTOM_APPS = []

INSTALLED_APPS = INSTALLED_APPS + CORE_APPS + CUSTOM_APPS + PLUGIN_APPS

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if int(os.environ.get("PROMETHEUS", 0)):
    MIDDLEWARE = PROMETHEUS_BEFORE_MIDDLEWARE + MIDDLEWARE + PROMETHEUS_AFTER_MIDDLEWARE

ROOT_URLCONF = "django_app.urls"

WSGI_APPLICATION = "django_app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("SQL_DATABASE", "sample_db_dev"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST", "django_db"),
        "PORT": os.environ.get("SQL_PORT", 5432),
    }
}

# Redis Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f'redis://{os.environ.get("REDIS_CACHED")}',
    }
}

# Celery Broker
CELERY_BROKER = f'redis://{os.environ.get("REDIS_BROKER", "localhost:6379")}'
CELERY_BROKER_URL = CELERY_BROKER
CELERY_RESULT_BACKEND = CELERY_BROKER
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_ROUTES = {
    "apps.core.files.tasks.long_task": {"queue": "long_queue"},
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Manila"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
LOGGING_PATH = os.environ.get("LOGGING_PATH", "app.log")
REQUESTS_LOGGING_PATH = os.environ.get("LOGGING_PATH", "requests.log")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": CustomisedJSONFormatter}},
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGGING_PATH,
            "maxBytes": 1024 * 1024 * 20,  # 20 MB,
            "backupCount": 2,
            "formatter": "json",
        },
        "requestlogs_to_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 20,  # 20 MB,
            "backupCount": 2,
            "filename": REQUESTS_LOGGING_PATH,
        },
    },
    "root": {"handlers": ["default"], "level": "DEBUG"},
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "requestlogs": {
            "handlers": ["requestlogs_to_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

LOGIN_REDIRECT_URL = "login"
LOGOUT_REDIRECT_URL = "login"

# REST FRAMEWORK
REST_FRAMEWORK = {
    "PAGE_SIZE": 50,
    "ORDERING_PARAM": "order_by",
    "PAGE_PARAM": "page",
    "SEARCH_PARAM": "q",
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework_json_api.renderers.JSONRenderer",),
    # 'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
}

# EMAIL SETTINGS via Sendgrid
EMAIL_HOST = os.getenv("SENDGRID_HOST", "smtp.sendgrid.net")
EMAIL_REST_HOST = os.getenv(
    "SENDGRID_REST_HOST", "https://api.sendgrid.com/v3/mail/send"
)
EMAIL_HOST_USER = os.getenv("SENDGRID_HOST_USER", "apikey")
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_HOST_PASSWORD", "")
EMAIL_PORT = os.getenv("SENDGRID_PORT", 465)
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = os.getenv("ADMIN_EMAIL", "admin@sample.com")
EMAIL_SEND = int(os.getenv("EMAIL_SEND", 0))

# REGISTRATION SETTINGS
EMAIL_REGISTRATION_TEMPLATE = "email/registration/registration_success"
EMAIL_REGISTRATION_SUBJECT = (
    f"User Registration: You have been registered to Django App"
)
EMAIL_REGISTRATION_BCC = ""

# SITE_URL
SITE_URL = "http://localhost:8000"

# STORAGE MECHANISM
DEFAULT_FILE_STORAGE = os.environ.get(
    "DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage"
)
MEDIA_ROOT = os.path.join(BASE_DIR, "files")
MEDIA_URL = "/uploaded/"
