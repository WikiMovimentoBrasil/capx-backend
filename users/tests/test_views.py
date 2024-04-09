import profile
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import Profile, CustomUser
from users.serializers import ProfileSerializer

class ProfileViewSetTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password='123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_users_list(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_profile_detail(self):
        response = self.client.get('/profile/' + str(self.user.pk) + '/')
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles.first())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_profile(self):
        url = '/profile/' + str(self.user.pk) + '/'
        updated_data = {
            'about': 'first user ever!',
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles.first())
        self.assertEqual(serializer.data['about'], updated_data['about'])

    def test_destroy_profile(self):
        response = self.client.delete('/profile/' + str(self.user.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_profile(self):
        response = self.client.post('/profile/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_other_profile(self):
        user = CustomUser.objects.create_user(username='test2', password='123')
        self.assertNotEqual(user.pk, self.user.pk)

        url = '/profile/' + str(user.pk) + '/'
        updated_data = {
            'about': 'second user ever!',
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
