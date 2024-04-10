from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from bugs.models import Bug, Attachment
from users.models import CustomUser
from bugs.serializers import BugSerializer, BugStaffSerializer, AttachmentSerializer
from django.core.files.uploadedfile import SimpleUploadedFile


class BugViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password='123')
        self.client = APIClient()

    def test_bug_list_unauthenticated(self):
        response = self.client.get('/bugs/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_bug_create_unauthenticated(self):
        bug_data = {
            'title': 'New Bug',
            'description': 'New Bug Description',
        }

        response = self.client.post('/bugs/', bug_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'test')
        self.assertIsInstance(self.user, CustomUser)
        self.assertTrue(self.user.is_active)

    def test_bug_create_authenticated(self):
        bug_data = {
            'title': 'New Bug',
            'description': 'New Bug Description',
        }

        self.client.force_authenticate(self.user)
        response = self.client.post('/bugs/', bug_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bug_list_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/bugs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AttachmentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password='123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.client.post('/bugs/', {'title': 'Bug', 'description': 'Bug',})
        attachment_data = {
            'file': SimpleUploadedFile('attachment.txt', b'attachment content'),
            'bug': '1',
        }
        self.client.post('/attachment/', attachment_data)

    def test_attachment_list(self):
        response = self.client.get('/attachment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_attachment_retrieve(self):
        attachment_id = 1
        response = self.client.get(f'/attachment/{attachment_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file'].split('/')[-1].split('_')[0], 'attachment')

    def test_attachment_create(self):
        attachment_data = {
            'file': SimpleUploadedFile('new_attach.txt', b'new attachment content'),
            'bug': '1',
        }
        response = self.client.post('/attachment/', attachment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_attachment_update(self):
        attachment_data = {
            'file': SimpleUploadedFile('updated_attachment.txt', b'updated attachment content'),
            'bug': '1',
        }
        response = self.client.put(f'/attachment/1/', attachment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file'].split('/')[-1].split('_')[0], 'updated')

    def test_attachment_delete(self):
        response = self.client.delete(f'/attachment/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



        
