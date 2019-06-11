from .base import *

DEBUG = True

SECRET_KEY = 'SECRET'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'FGR_LOCAL_DB',
        'USER': 'fgr_local_user',
        'PASSWORD': 'SECRET',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_SECRET',
        }
    }
}
