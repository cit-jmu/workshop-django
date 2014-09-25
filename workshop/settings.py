"""
Django settings for workshop project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# set environment, default to 'development'
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'profiles'
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

AUTHENTICATION_BACKENDS = (
  'auth.backends.LDAPBackend',
  'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'workshop.urls'

WSGI_APPLICATION = 'workshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# For databases other than sqlite that require a username and password,
# put the configuration in secrets.py.  This is left as a default.
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}
import dj_database_url
DATABASES = { 'default': dj_database_url.config() }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
)

# Logging
# https://docs.djangoproject.com/en/1.7/topics/logging/
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'standard': {
      'format': '[%(asctime)s] %(levelname)s (%(name)s:%(lineno)s) %(message)s'
    },
  },
  'handlers': {
    'file': {
      'level': 'DEBUG',
      'class': 'logging.FileHandler',
      'filename': "log/%s.log" % DJANGO_ENV,
      'formatter': 'standard',
    },
  },
  'loggers': {
    'workshop': {
      'handlers': ['file'],
      'level': 'DEBUG',
    }
  },
}

LDAP_AUTH = {
  'uri': "ldap://ldap.ad.jmu.edu",
  'secure': True,
  'base': "ou=JMUma,dc=ad,dc=jmu,dc=edu",
  'search_filter': "sAMAccountName=%s",
  'attrlist': (
    'givenName', 'sn', 'mail', 'telephoneNumber', 'postOfficeBox', 'ou',
    'eduPersonAffiliation', 'jmunickname',
  ),
  'local_admin_user': "admin",
}

# import environment settings, these will overwrite any default settings above
from importlib import import_module
try:
  module = import_module("workshop.environments.%s" % DJANGO_ENV)
  for setting in dir(module):
    # assume that all valid settings are uppercase, following Django standards
    # this also eliminates things like '__name__' or '__file__'
    if setting == setting.upper(): locals()[setting] = getattr(module, setting)
except:
  pass
