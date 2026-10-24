"""Isolated tests: never connect to the configured production database."""
import os

os.environ.setdefault('DJANGO_DEBUG', 'true')
os.environ.setdefault('DJANGO_SECRET_KEY', 'test-only-key-not-for-deployment-12345678901234567890')
from .settings import *  # noqa: F403,E402

if os.environ.get('PREDICTOR_TEST_MYSQL') != '1':
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
