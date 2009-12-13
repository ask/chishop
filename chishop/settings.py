from conf.default import *
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOCAL_DEVELOPMENT = True

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
