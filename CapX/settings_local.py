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
        message = 'You are running in production mode'

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

    else:
        debug = True
        hosts = ['127.0.0.1']
        callback = 'http://127.0.0.1:8000/oauth/complete/mediawiki/'
        message = 'You are running in local mode, please make sure to set up the replica.my.cnf file to run in production mode'

        databases = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME':  Path(__file__).resolve().parent.parent / 'db.sqlite3',
            }
        }

    return {
        'DEBUG': debug,
        'ALLOWED_HOSTS': hosts,
        'SOCIAL_AUTH_MEDIAWIKI_CALLBACK': callback,
        'DATABASES': databases,
        'MESSAGE': message,
    }

settings = configure_settings()
DEBUG = settings['DEBUG']
ALLOWED_HOSTS = settings['ALLOWED_HOSTS']
SOCIAL_AUTH_MEDIAWIKI_CALLBACK = settings['SOCIAL_AUTH_MEDIAWIKI_CALLBACK']
DATABASES = settings['DATABASES']
print(settings['MESSAGE'])
