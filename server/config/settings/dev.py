from .base import *

# Debug mode ON for development
DEBUG = True

# Allow local access only
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# In dev, allow everything for simplicity
CORS_ALLOW_ALL_ORIGINS = True
