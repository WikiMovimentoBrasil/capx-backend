import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
HOME = os.environ.get('HOME') or ""
SECRET_KEY = os.environ.get("SECRET_KEY")
SOCIAL_AUTH_MEDIAWIKI_URL = 'https://meta.wikimedia.org/w/index.php'
SOCIAL_AUTH_MEDIAWIKI_KEY = os.environ.get("SOCIAL_AUTH_MEDIAWIKI_KEY")
SOCIAL_AUTH_MEDIAWIKI_SECRET = os.environ.get("SOCIAL_AUTH_MEDIAWIKI_SECRET")
LANGUAGES = (
    ('en', 'English'),
    ('pt-br', 'Brazilian Portuguese'),
    ('pt', 'Portuguese'),
    ('es', 'Spanish'),
)

def configure_settings():
    if os.path.exists(HOME + '/replica.my.cnf'):
        debug = False
        hosts = ['capx-backend.toolforge.org','toolforge.org']
        callback = 'https://capx.toolforge.org/oauth/'

        databases = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get("TOOL_TOOLSDB_USER") + '__capx', # type: ignore
                'USER': os.environ.get("TOOL_TOOLSDB_USER"),
                'PASSWORD': os.environ.get("TOOL_TOOLSDB_PASSWORD"),
                'HOST': 'tools.db.svc.wikimedia.cloud',
                'PORT': '',
            }
        }

        opensearch={
            'default': {
                'hosts': 'http://elasticsearch.svc.tools.eqiad1.wikimedia.cloud:80',
                'http_auth': (
                    os.environ.get("TOOL_ELASTICSEARCH_USER", "default-value"), 
                    os.environ.get("TOOL_ELASTICSEARCH_PASSWORD", "default-value")
                )
            }
        }

    else:
        debug = True
        hosts = ['127.0.0.1']
        callback = 'http://127.0.0.1:8000/oauth/complete/mediawiki/'

        databases = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME':  Path(__file__).resolve().parent.parent / 'db.sqlite3',
            }
        }

        opensearch={
            'default': {
                'hosts': 'http://localhost:9200'
            }
        }

    return {
        'DEBUG': debug,
        'ALLOWED_HOSTS': hosts,
        'SOCIAL_AUTH_MEDIAWIKI_CALLBACK': callback,
        'DATABASES': databases,
        'OPENSEARCH_DSL': opensearch,
    }

settings = configure_settings()
DEBUG = settings['DEBUG']
ALLOWED_HOSTS = settings['ALLOWED_HOSTS']
SOCIAL_AUTH_MEDIAWIKI_CALLBACK = settings['SOCIAL_AUTH_MEDIAWIKI_CALLBACK']
DATABASES = settings['DATABASES']
OPENSEARCH_DSL = settings['OPENSEARCH_DSL']
if DEBUG == True:
    print('replica.my.cnf file not found, running as local')
else:
    print('replica.my.cnf file found, running as production')
