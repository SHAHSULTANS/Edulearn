from jobapp.settings import *

from decouple import config

SECRET_KEY = config('SECRET_KEY')



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # or mysql
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),  # optional cast
    }
}