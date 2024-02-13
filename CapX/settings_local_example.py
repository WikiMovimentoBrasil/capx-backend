SECRET_KEY = '<YOUR VERY SECRET KEY>'
DEBUG = False
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
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print('replica.my.cnf file not found')
