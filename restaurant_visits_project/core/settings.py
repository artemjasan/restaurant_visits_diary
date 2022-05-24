import datetime
import os
from distutils.util import strtobool
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django_project_secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DEBUG", "True"))

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]


# Application definition
INSTALLED_APPS = [
    # Inner Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Inner apps
    'v1.diary.apps.DiaryConfig',

    # 3rd party apps
    'rest_framework',

    # Authentication
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "drf_yasg",

    # Allauth required
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

# Is required for allauth for registration
# https://django-allauth.readthedocs.io/en/latest/installation.html
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "diary"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Settings for JWT
# https://dj-rest-auth.readthedocs.io/en/latest/installation.html#json-web-token-jwt-support-optional
REST_USE_JWT = True
JWT_AUTH_COOKIE = "diary-auth"
JWT_AUTH_REFRESH_COOKIE = "diary-refresh-token"
# For entry task purposes it is OK that it is disabled
ACCOUNT_EMAIL_VERIFICATION = "none"
# JWT_AUTH_SECURE - If you want the cookie to be only sent to the server
# when a request is made with the https scheme (default: False).
JWT_AUTH_SECURE = False
# Every time user refreshes their token, new refresh-token is provided
SIMPLE_JWT = {"REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=30), "ROTATE_REFRESH_TOKENS": True}
