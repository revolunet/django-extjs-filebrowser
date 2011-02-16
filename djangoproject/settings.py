# -*- encoding: utf8 -*-

# import local settings
try:
    from local_settings import *

except ImportError, exp:
    print "ERROR IMPORTING LOCALSETTINGS"
    pass


# Django settings for easyintranet project.
import os, sys

 

TEMPLATE_DEBUG = DEBUG
MANAGERS = ADMINS
USE_MULTITHREADED_SERVER = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'core', 'static')
MEDIA_URL = '/static/'

APPEND_SLASH = False

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en-EN'
SITE_ID = 1
USE_I18N = True

# see http://code.djangoproject.com/browser/django/trunk/django/conf/global_settings.py
gettext = lambda s: s
LANGUAGES = (
  ('en', gettext('Anglais')),
  ('fr', gettext(u'Français')),
)


SEND_BROKEN_LINK_EMAILS = True
#IGNORABLE_404_ENDS = ('.ico')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'apps.django_extjs_filebrowser',
    'core.django_concurrent_test_server'   # only for DEV !
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 #'django.middleware.locale.LocaleMiddleware',
# 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'core.AJAXSimpleExceptionResponse.AJAXSimpleExceptionResponse'
 #'django.contrib.messages.middleware.MessageMiddleware',
 )
 
 
ROOT_URLCONF = 'core.urls'
