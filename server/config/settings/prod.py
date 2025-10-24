from .base import *
from decouple import config

# Debug OFF for production
DEBUG = False

# Explicitly set your production hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Set allowed CORS origins
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')

# Optional: secure cookies, headers
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
