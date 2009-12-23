from conf.default import *
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('chishop', 'example@example.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'chishop'
DATABASE_USER = 'chishop'
DATABASE_PASSWORD = 'chishop'
DATABASE_HOST = ''
DATABASE_PORT = ''
