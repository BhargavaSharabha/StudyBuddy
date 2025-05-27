"""
Development settings for ProjStudyBuddy project.
"""

from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-@7z&5=u)9ut62w&9fa8!#ww^$34dv74q767w+wdt&+ix_-$ta4')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '5b27-129-119-235-16.ngrok-free.app']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email settings - Console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CSRF settings for development
CSRF_TRUSTED_ORIGINS = [
    'https://5b27-129-119-235-16.ngrok-free.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# Development-specific logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
} 