"""
Build settings for ProjStudyBuddy project.
Used during Docker build process when environment variables are not available.
"""

from .base import *

# Minimal settings for build process
SECRET_KEY = 'build-time-secret-key-not-for-production'
DEBUG = False
ALLOWED_HOSTS = ['*']

# Use SQLite for build (we don't actually connect to it during collectstatic)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable security features that require environment variables
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email backend for build
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CSRF settings for build
CSRF_TRUSTED_ORIGINS = []

# Logging for build
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