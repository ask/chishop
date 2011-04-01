# Django settings for djangopypi project.
import os

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

# Allow uploading a new distribution file for a project version
# if a file of that type already exists.
#
# The default on PyPI is to not allow this, but it can be real handy
# if you're sloppy.
DJANGOPYPI_ALLOW_VERSION_OVERWRITE = False
DJANGOPYPI_RELEASE_UPLOAD_TO = 'dists'

# change to False if you do not want Django's default server to serve static pages
LOCAL_DEVELOPMENT = True

REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = "/"

EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = DEFAULT_FROM_EMAIL

MANAGERS = ADMINS

DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
here = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
MEDIA_ROOT = os.path.join(here, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w_#0r2hh)=!zbynb*gg&969@)sy#^-^ia3m*+sd4@lst$zyaxu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'chishop.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.admindocs',
    'registration',
    'djangopypi',
)
