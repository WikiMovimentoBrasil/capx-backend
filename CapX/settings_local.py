import os
import configparser
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

DEBUG = False #Change to False when in production

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
HOME = os.environ.get('HOME') or ""
SECRET_KEY = os.environ.get("SECRET_KEY")
SOCIAL_AUTH_MEDIAWIKI_URL = 'https://meta.wikimedia.org/w/index.php'
SOCIAL_AUTH_MEDIAWIKI_KEY = os.environ.get("SOCIAL_AUTH_MEDIAWIKI_KEY")
SOCIAL_AUTH_MEDIAWIKI_SECRET = os.environ.get("SOCIAL_AUTH_MEDIAWIKI_SECRET")
SOCIAL_AUTH_MEDIAWIKI_CALLBACK = 'oob'


if os.path.exists(HOME + '/replica.my.cnf'):
    ALLOWED_HOSTS = ['capacity-exchange.toolforge.org','toolforge.org']
    SOCIAL_AUTH_MEDIAWIKI_CALLBACK = 'https://capacity-exchange.toolforge.org/oauth/complete/mediawiki/'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get("TOOL_TOOLSDB_USER") + '__capx',
            'USER': os.environ.get("TOOL_TOOLSDB_USER"),
            'PASSWORD': os.environ.get("TOOL_TOOLSDB_PASSWORD"),
            'HOST': 'tools.db.svc.wikimedia.cloud',
            'PORT': '',
        }
    }

    ELASTICSEARCH_DSL={
        'default': {
            'hosts': 'http://elasticsearch.svc.tools.eqiad1.wikimedia.cloud:80',
            'http_auth': (
                os.environ.get("TOOL_ELASTICSEARCH_USER", "default-value"), 
                os.environ.get("TOOL_ELASTICSEARCH_PASSWORD", "default-value")
            )
        }
    }

else:
    ALLOWED_HOSTS = ['127.0.0.1']
    SOCIAL_AUTH_MEDIAWIKI_CALLBACK = 'http://127.0.0.1:8000/oauth/complete/mediawiki/'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':  Path(__file__).resolve().parent.parent / 'db.sqlite3',
        }
    }

    ELASTICSEARCH_DSL={
        'default': {
            'hosts': 'http://localhost:9200'
        }
    }
    print('replica.my.cnf file not found, running as local')

LANGUAGES = (
    ('en', _('English')),
    ('pt-br', _('Brazilian Portuguese')),
    ('pt', _('Portuguese')),
    ('es', _('Spanish')),
)
