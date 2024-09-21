from django.test import TestCase
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth
from rest_framework.test import APIClient
from unittest.mock import patch
from django.urls import reverse
from social_core.exceptions import AuthException
import jwt
from users.models import Profile  # Assuming you have a Profile model associated with the user

CustomUser = get_user_model()

class AccountCreationWorkflowTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
        }
        self.social_auth_data = {
            'provider': 'mediawiki',
            'uid': '1234567890',
        }

    def test_account_creation_on_first_login(self):
        # Simulate social authentication and user creation
        user = CustomUser.objects.create(**self.user_data)
        UserSocialAuth.objects.create(user=user, **self.social_auth_data)

        # Ensure user was created
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(UserSocialAuth.objects.count(), 1)

        # Check that the user profile was created
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
        
        # Check that the user has the correct attributes (you can add more checks as needed)
        self.assertEqual(profile.user.username, self.user_data['username'])
        self.assertEqual(profile.user.email, self.user_data['email'])
