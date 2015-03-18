"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import LOGIN_REDIRECT_URL
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '74&479nvpwd&#&+y&)*f*faf+tfe_@+pww%d#qgf11wcl+65@h'

DEBUG=False
# DYNO will not be in os eviornment on local but will be on heroku
if not 'DYNO' in os.environ:
	DEBUG=True

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['localhost', 'pollportal.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #my apps
    'polls',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite')
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL='/static/'
STATIC_ROOT= os.path.join(BASE_DIR, 'static')
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Bobby's Amazon webservice credentials for media
AWS_ACCESS_KEY_ID = 'AKIAJP3MBZRMYA4HD2TA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'bobbysdebate'

DEFAULT_FILE_STORAGE = 'mysite.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'mysite.s3utils.StaticRootS3BotoStorage'


ADMINS = (
    ('Poll Portal Admin', 'virinchi.balabhadrapatruni@gmail.com'),
    ('Poll Portal Admin', 'bobbydonald25@gmail.com'),   # email will be sent to your_email
)

MANAGERS = ADMINS
