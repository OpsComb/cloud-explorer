"""
Contains production overrides
"""

import os
from pathlib import Path
from typing import List

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a=r9g&!u^n*&skA^SFHftm!-kjhzsdjk*b286j+*qlqp3y^v^2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS: List[str] = ['*']

ADMINS: List[tuple] = [('DevOps', 'admin@cloud_explorer.com')]

# to prevent clickjacking https://docs.djangoproject.com/en/2.2/ref/clickjacking/
X_FRAME_OPTIONS = 'DENY'

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    # will not be served, more like long term storage
    os.path.join(BASE_DIR, "static-storage"),
]

EMAIL_SUBJECT_PREFIX = "[Update from Cloud Explorer]"

EMAIL_USE_LOCALTIME = True

# EMAIL_HOST = "<add your email host here>"


# This is only used if BrokenLinkEmailsMiddleware is enabled
IGNORABLE_404_URLS = ["*favicon.ico$"]


STATIC_URL = '/static/'

# will be served
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static-serve")

THROTTLING_CACHE_BACKEND = "redis"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cwt_cache'
    },
    'redis': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # location can be a list in case of multiple clients
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "ce"
    }
}

DJANGO_REDIS_IGNORE_EXCEPTIONS = True

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'cloud_explorer.utils.throttling.PerUserThrottling'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day'
    }
}

CSRF_COOKIE_SECURE = True
