from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from orgs.models import OrganizationType
from users.models import CustomUser
from users.submodels import Region


class OrganizationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password='123')
        self.client = APIClient()
        OrganizationType.objects.create(type_name='Type 1', type_code='TYPE1')
        Region.objects.create(region_name='Region 1')
    
    def test_get_orgs_list_unauthenticated(self):
        response = self.client.get('/organizations/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_org_unauthenticated(self):
        org_data = {
            'display_name': 'New Organization',
            'acronym': 'NO',
            'type': '1',
            'territory': '1',
        }

        response = self.client.post('/organizations/', org_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_org_authenticated(self):
        org_data = {
            'display_name': 'New Organization',
            'acronym': 'NO',
            'type': '1',
            'territory': '1',
        }

        self.client.force_authenticate(self.user)
        response = self.client.post('/organizations/', org_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_org_staff(self):
        org_data = {
            'display_name': 'New Organization',
            'acronym': 'NO',
            'type': '1',
            'territory': '1',
        }

        self.user.is_staff = True
        self.client.force_authenticate(self.user)
        response = self.client.post('/organizations/', org_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_orgs_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/organizations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
