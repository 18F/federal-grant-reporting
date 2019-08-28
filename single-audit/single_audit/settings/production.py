from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG is currently only turned on in dev settings, but better safe than sorry.
DEBUG = False
