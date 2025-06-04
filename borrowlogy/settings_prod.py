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
        'PORT': 56801,  # Changed to integer (though both string and int work)
        'OPTIONS': {
            'sslmode': 'require',  # Enforces SSL encryption
            # 'hostaddr' is not typically needed if you're using 'HOST'
            # 'connect_timeout' is good for production
        },
        'CONN_MAX_AGE': 600,  # Increased from 60 (better for production)
        # 'CONN_HEALTH_CHECKS' is not a standard Django setting (remove)
        # 'DISABLE_SERVER_SIDE_CURSORS' is misspelled (corrected below)
        'DISABLE_SERVER_SIDE_CURSORS': False,  # Typically better performance when False
    }
}

# DATABASES = {
#     'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'), conn_max_age=600)
# }


# DATABASES = {
#     'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'), conn_max_age=600)
# }


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