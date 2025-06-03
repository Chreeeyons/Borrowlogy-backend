from .settings import *

DEBUG = False

# Get the domain from Railway
ALLOWED_HOSTS = ['*']  # You can restrict this to your Railway domain later

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',  # Replace with your frontend domain
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} 