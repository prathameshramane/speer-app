from .base import *
from decouple import config

DEBUG = False

ALLOWED_HOSTS = [
    config('PUBLIC_IP'),
    config('PUBLIC_ENDPOINT'),
    config('WWW_PUBLIC_ENDPOINT')
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
    }
}