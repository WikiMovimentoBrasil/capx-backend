from django.conf import settings
from django.test import TestCase
from ..settings_local import *


class SettingsLocalTestCase(TestCase):
    def test_allowed_hosts(self):
        self.assertEqual(settings.ALLOWED_HOSTS, ['127.0.0.1', 'testserver'])

    def test_social_auth_mediawiki_callback(self):
        self.assertEqual(settings.SOCIAL_AUTH_MEDIAWIKI_CALLBACK, 'http://127.0.0.1:8000/oauth/complete/mediawiki/')

    def test_default_database_engine(self):
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')

    def test_default_database_name(self):
        self.assertIsNotNone(settings.DATABASES['default']['NAME'])

    def test_opensearch_dsl_hosts(self):
        self.assertEqual(settings.OPENSEARCH_DSL['default']['hosts'], 'http://localhost:9200')

    def test_languages(self):
        expected_languages = (
            ('en', 'English'),
            ('pt-br', 'Brazilian Portuguese'),
            ('pt', 'Portuguese'),
            ('es', 'Spanish'),
        )
        self.assertEqual(settings.LANGUAGES, expected_languages)