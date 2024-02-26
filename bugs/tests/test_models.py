from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from ..models import Bug, Attachment
from users.models import CustomUser

class BugModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for the foreign key requirement
        test_user = CustomUser.objects.create_user(username='testuser', password='12345')
        test_user.save()

        # Create a Bug instance to use in tests
        Bug.objects.create(
            user=test_user,
            title='Sample Bug',
            description='Sample Description',
            bug_type='error',
            status='to_do'
        )

    def test_bug_content(self):
        bug = Bug.objects.get(id=1)
        expected_user = f'{bug.user}'
        expected_title = f'{bug.title}'
        expected_description = f'{bug.description}'
        expected_bug_type = f'{bug.bug_type}'
        expected_status = f'{bug.status}'

        self.assertEqual(expected_user, 'testuser')
        self.assertEqual(expected_title, 'Sample Bug')
        self.assertEqual(expected_description, 'Sample Description')
        self.assertEqual(expected_bug_type, 'error')
        self.assertEqual(expected_status, 'to_do')