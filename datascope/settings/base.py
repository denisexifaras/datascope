import logging
log = logging.getLogger(__name__)

try:
    from setup import *
except ImportError:
    log.warning("Could not import setup settings. Are they created?")
try:
    from secrets import *
except ImportError:
    log.warning("Could not import secret settings. Are they created?")

DEBUG = False
REQUESTS_PROXIES = None
REQUESTS_VERIFY = True
REQUESTS_PROXIES_ENABLED = {
    "http": "localhost:8888"
}

MAX_BATCH_SIZE = 1000
PATH_TO_LOGS = PATH_TO_PROJECT + "system/logs/"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 3rd party
    'djcelery',
    'rest_framework',
    # Main app
    'datascope',
    # Framework apps
    'core',
    'sources',
    'legacy',
    # Algorithms
    'wiki_news',
    'visual_translations',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': PATH_TO_PROJECT + 'datascope.db',  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '.localhost',
    '.globe-scope.com',
    '.globe-scope.org',
    '.data-scope.com',
    '.data-scope.org',
]

APPEND_SLASH = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False
DATETIME_FORMAT = 'd-m-y H:i:s/u'  # default would get overridden by L18N

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Available languages for all projects
ugettext = lambda s: s # a dummy ugettext to prevent circular import
LANGUAGES = (
    ('en', ugettext('English')),
    ('pt', ugettext('Portuguese')),
    ('nl', ugettext('Dutch')),
    ('de', ugettext('German')),
    ('es', ugettext('Spanish')),
    ('fr', ugettext('French')),
)

LOCALE_PATHS = (
    PATH_TO_PROJECT + 'src/locale/',
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = SERVER_ROOT + 'media/' + PROJECT_NAME + '/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/' + PROJECT_NAME + '/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = SERVER_ROOT + 'static/' + PROJECT_NAME + '/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/' + PROJECT_NAME + '/'

# Additional locations of static files
STATICFILES_DIRS = (
    PATH_TO_PROJECT + 'legacy/output/http/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Datascope middleware
    'core.middleware.origin.AllowOriginMiddleware',
)

ROOT_URLCONF = 'datascope.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'datascope.wsgi.application'

FIXTURE_DIRS = (
    PATH_TO_PROJECT + 'core/tests/fixtures/',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s in %(module)s: %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'datascope': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

TEST_RUNNER = "core.tests.runner.DataScopeDiscoverRunner"

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    #'DEFAULT_PAGINATION_CLASS': 'core.views.content.ContentPagination',
    'PAGE_SIZE': 100,
}

# Celery settings
import djcelery
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_RESULT_BACKEND = "djcelery.backends.database.DatabaseBackend"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.fakoberkers.nl"
EMAIL_PORT = 587

import requests.packages.urllib3.contrib.pyopenssl
requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()

#######################################################
# LEGACY SETTINGS
#######################################################

TEMPLATE_DIRS = (
    PATH_TO_PROJECT + "legacy/output/http/html",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

HIF_SKIP_EXTERNAL_RESOURCE_INTEGRATION_TESTS = True