# Django settings for comebh project.

import os
import os.path
import datetime
from decimal import Decimal

ADMINS = (
    ('Gabriel Poesia', 'gabriel.poesia@gmail.com'),
)


MANAGERS = ADMINS

if os.environ.get('APPLICATION_ENVIRONMENT') in (None, 'development'):
    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'comebh2',
            'USER': 'comebh',
            'PASSWORD': 'comebh',
            'HOST': '',
            'PORT': '',
        }
    }

    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1000
    EMAIL_HOST_USER = "comebh+dajnoroeste.juventudeespirita.com.br"
    EMAIL_HOST_PASSWORD = ""
    DEFAULT_FROM_EMAIL = "comebh@dajnoroeste.juventudeespirita.com.br"
    EMAIL_FROM_NAME = "COMEBH Noroeste (teste)"

    EMAIL_REMOTE_SENDER = "http://localhost:8080/email/enviar"
    EMAIL_TOKEN = "127003923520501950085302456561080789870"

    SITE_URL = "http://localhost:8000"

    PAGSEGURO_EMAIL_CONTA = "gabriel.poesia@gmail.com"
    PAGSEGURO_TOKEN = "7D8E77121250467A9705056AD5ED0DEA"
    VALOR_INSCRICAO = Decimal("1.00")
    VALOR_CAMISA = Decimal("0.50")



elif os.environ.get('APPLICATION_ENVIRONMENT') == 'production':
    DEBUG = False 

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
           'NAME': 'inscricao',
            'USER': 'admin',
            'PASSWORD': 'rdBGsSYL2B-k',
            'HOST': '127.4.10.129',
            'PORT': '3306',
        }
    }

    EMAIL_REMOTE_SENDER = "http://mailer.juventudeespirita.com.br/email/enviar"
    EMAIL_TOKEN = "127003923520501950085302456561080789870"
    DEFAULT_FROM_EMAIL = "comebh@dajnoroeste.juventudeespirita.com.br"
    EMAIL_FROM_NAME = "COMEBH Noroeste"

    SITE_URL = "http://inscricao-comebh.rhcloud.com"

    VALOR_INSCRICAO = Decimal("30.00")
    VALOR_CAMISA = Decimal("10.00")

    PAGSEGURO_TOKEN = "6C0D8CC7A6554E009BE36C52C5F162EC"
    PAGSEGURO_EMAIL_CONTA = "daj_noroeste@juventudeespirita.com.br"


TEMPLATE_DEBUG = DEBUG

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "/home/gpoesia/Dropbox/workspace/COMEBH/inscricao_django/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.    
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1hkm6!akkp4nl-!lfm@3z07@)9by4r!p=x5i5byeab6t2rooit'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'comebh.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'comebh.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), os.path.pardir, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'inscricao',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DEFAULT_CHARSET = "UTF-8"

LOGIN_URL = "/login"

DATA_COMEBH = datetime.date(2013, 2, 9)
