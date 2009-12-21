from conf.default import *
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOCAL_DEVELOPMENT = True

# Allow uploading a new distribution file for a project version
# if a file of that type already exists.
#
# The default on PyPI is to not allow this, but it can be real handy
# if you're sloppy.
#PYPI_ALLOW_VERSION_OVERWRITE = False

# What subdirectory to store distributions in.
#PYPI_RELEASE_UPLOAD_TO = 'dists'


PYPI_ROLES = {"default": (),
              "staging": ("default", )}
SITE_DOMAIN = "localhost"

if LOCAL_DEVELOPMENT:
    import sys
    sys.path.append(os.path.dirname(__file__))

ADMINS = (
     ('chishop', 'example@example.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(here, 'devdatabase.db')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''


TEMPLATE_CONTEXT_PROCESSORS += ("djangopypi.context_processors.role_from_subdomain",)
