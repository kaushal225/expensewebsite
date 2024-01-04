"""
Django settings for expensewebsite project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from pathlib import Path
import os
from django.contrib import messages
import dj_database_url
from dotenv import load_dotenv
from django.conf import global_settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')#'django-insecure-hh#_5qlzly8z6c-qeg=y$5bowfx98v2!st=d0_7al+6s@qu(to'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS=[
    "http://localhost",
    "http://0.0.0.0",
    "https://expensewebsite-production.up.railway.app/",
    "https://expensewebsite-production.up.railway.app"
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'expenses',
    'userpreferences',
    'income',
    'groups',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'expensewebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'expensewebsite.wsgi.application'

load_dotenv('.env')

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASE_URL=os.environ.get('DATABASE_URL')
DATABASES = {
   "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))

    #"default": {
    #    "ENGINE": "django.db.backends.postgresql",
    #    "URL":os.environ.get('DATABASE_URL'),
    #    "NAME": os.environ.get('DB_NAME'),
    #    "USER": os.environ.get('DB_USER'),
    #    "PASSWORD": os.environ.get('DB_USER_PASSWORD'),
    #    "HOST": os.environ.get('DB_HOST'),
    #    "PORT": os.environ.get('DB_PORT'),
    #}
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

#STATIC_URL = 'static/'
#STATICFILES_DIRS=[os.path.join(BASE_DIR,'expensewebsite/static')]
#STATIC_ROOT=os.path.join(BASE_DIR,'static')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
 #it was before editing

#after editing

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "expensewebsite/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

print(STATIC_ROOT)


MESSAGE_TAGS={
    messages.ERROR:'danger'
}


REST_FRAMEWORK={
    'DEFAULT_THROTTLE_CLASSES':[
        'rest_framework.throttling.UserRateThrottle'
    ],

    'DEFAULT_THROTTLE_RATES':{
        'automation':'1/day'
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('email_host_user')
EMAIL_HOST_PASSWORD =os.environ.get('email_host_password')
EMAIL_USE_TLS =True
DEFAULT_FROM_EMAIL = os.environ.get('email_host_user')
#print(DATABASES['default'])


