from .settings import *
import os

DEBUG = False

# Get the domain from Railway
ALLOWED_HOSTS = ['*']

# Security settings
SECURE_SSL_REDIRECT = False  # Disable SSL redirect for Railway
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'https://*.railway.app',
    'http://localhost:3000',
]

# Database - Use environment variables for database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'cWPoWKSXbAgdUKNzKCoJhOiXzXGQYFWv',
        'HOST': 'metro.proxy.rlwy.net',
        'PORT': '56801',
        'OPTIONS': {
            'sslmode': 'require',
            'connect_timeout': 10,
            'hostaddr': 'metro.proxy.rlwy.net',  # Force TCP/IP connection
        },
        'CONN_MAX_AGE': 60,
        'CONN_HEALTH_CHECKS': True,
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
} 