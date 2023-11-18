from .base import *

DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = "django-insecure-eufdalwqu=gfv))!itu2*yp95tii95fuqp_8y7&m%u85ew4fhu"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    }
}

DEVELOPMENT_APPS = ["silk", "drf_spectacular"]

INSTALLED_APPS += DEVELOPMENT_APPS

MIDDLEWARE.insert(1, "silk.middleware.SilkyMiddleware")

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

STATIC_URL = "static/"
