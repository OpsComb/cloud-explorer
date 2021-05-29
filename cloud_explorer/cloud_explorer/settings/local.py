""" Local dev properties """
import os
from pathlib import Path

THROTTLING_CACHE_BACKEND = "default"

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

DJANGO_REDIS_IGNORE_EXCEPTIONS = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    # will not be served, more like long term storage
    os.path.join(BASE_DIR, "static-storage"),
]


# will be served
STATIC_ROOT = os.path.join(BASE_DIR, "static-serve")
