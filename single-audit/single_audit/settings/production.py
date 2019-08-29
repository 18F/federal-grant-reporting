from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG is currently only turned on in dev settings, but better safe than sorry.
DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] "
                      "%(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': "%(levelname)s %(message)s",
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/tock.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
        'django.template': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'uaa_client': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'tock-auth': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'tock-employees': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'tock-hours': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'tock-organizations': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'tock-projects': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'tock': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
    },
}
