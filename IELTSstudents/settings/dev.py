from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-te04#)qd(^l18b0sbti8dlvm^@*l%argc4t574c#ov4f-n%bgg'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ieltsstudents',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '1223',
    }
}