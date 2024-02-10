import os
import configparser
from pathlib import Path
from django.utils.translation import gettext_lazy as _

SECRET_KEY = '<YOUR VERY SECRET KEY>'
DEBUG = True #Change to False when in production
ALLOWED_HOSTS = ['<YOUR HOSTS>']
HOME = os.environ.get('HOME') or ""

SOCIAL_AUTH_MEDIAWIKI_KEY = '<YOUR MEDIAWIKI KEY>'
SOCIAL_AUTH_MEDIAWIKI_SECRET = '<YOUR MEDIAWIKI TOKEN'
SOCIAL_AUTH_MEDIAWIKI_URL = 'https://meta.wikimedia.org/w/index.php'
SOCIAL_AUTH_MEDIAWIKI_CALLBACK = '<YOUR HOST>/oauth/complete/mediawiki/'

BASE_DIR = Path(__file__).resolve().parent.parent

replica_path = HOME + '/replica.my.cnf'
if os.path.exists(replica_path):
    config = configparser.ConfigParser()
    config.read(replica_path)
    elasticsearch = configparser.ConfigParser()
    elasticsearch.read(HOME + '/.elasticsearch.ini')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '<YOUR DATABASE>',
            'USER': config['client']['user'],
            'PASSWORD': config['client']['password'],
            'HOST': 'tools.db.svc.wikimedia.cloud',
            'PORT': '',
        }
    }
    ELASTICSEARCH_DSL={
        'default': {
            'hosts': 'http://elasticsearch.svc.tools.eqiad1.wikimedia.cloud:80',
            'http_auth': (elasticsearch['username'] , elasticsearch['password'])
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ELASTICSEARCH_DSL={
        'default': {
            'hosts': 'https://localhost:9200',
            'http_auth': ('elastic', '<ELASTICSEARCH_PASSWORD>')
        }
    }
    print('replica.my.cnf file not found')

LANGUAGES = (
    ('en', _('English')),
    ('pt-br', _('Brazilian Portuguese')),
    ('pt', _('Portuguese')),
    ('es', _('Spanish')),
)
