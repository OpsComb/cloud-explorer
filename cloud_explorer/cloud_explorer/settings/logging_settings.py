from pathlib import Path

LOG_DIR = "logs/"

# make logs director if doesn't exist
filepath = Path(LOG_DIR)
filepath.mkdir(parents=True, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },

    'handlers': {
        'app-logs': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + "app.log",
            'maxBytes': 1024 * 1024 * 50,     # 50 MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + "/access.log",
            'maxBytes': 1024 * 1024 * 500,         # 50 MB
            'backupCount': 5,
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'aws': {
            'handlers': ['app-logs'],
            'level': 'INFO'
        },
        'cloud_explorer': {
            'handlers': ['app-logs'],
            'level': 'INFO'
        },
        'utils': {
            'handlers': ['app-logs'],
            'level': 'INFO'
        }
    }
}
