import secrets
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from orgs.models import OrganizationType, Organization
from users.models import CustomUser
from users.submodels import Territory


class OrganizationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password=str(secrets.randbits(16)))
        self.client = APIClient()
        OrganizationType.objects.create(type_name='Type 1', type_code='TYPE1')
        Territory.objects.create(territory_name='Territory 1')
    
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_orgs_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/organizations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.create(
            display_name='New Organization',
            acronym='NO',
            type=OrganizationType.objects.get(pk=1),
        )
        organization.territory.set([Territory.objects.get(pk=1)])
        response = self.client.get('/organizations/')
        self.assertEqual(len(response.data), 0)

        Organization.objects.create(
            display_name='New Organization 2',
            acronym='NO2', 
            type=OrganizationType.objects.get(pk=1),
        )
        organization.territory.set([Territory.objects.get(pk=1)])
        organization.managers.set([self.user])
        response = self.client.get('/organizations/')
        self.assertEqual(len(response.data), 1)


    def test_list_orgs_staff(self):
        self.user.is_staff = True
        self.client.force_authenticate(self.user)
        response = self.client.get('/organizations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        org_data = {
            'display_name': 'New Organization',
            'acronym': 'NO',
            'type': '1',
            'territory': '1',
        }
        self.client.post('/organizations/', org_data)
        response = self.client.get('/organizations/')
        self.assertEqual(len(response.data), 1)

    def test_retrieve_org(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/organizations/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        organization = Organization.objects.create(
            display_name='New Organization',
            acronym='NO',
            type=OrganizationType.objects.get(pk=1),
        )
        organization.territory.set([Territory.objects.get(pk=1)])
        response = self.client.get('/organizations/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.user.is_staff = True
        self.user.save()
        response = self.client.get('/organizations/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.is_staff = False
        self.user.save()
        organization.managers.set([self.user])
        response = self.client.get('/organizations/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_org(self):
        self.client.force_authenticate(self.user)
        response = self.client.put('/organizations/1/', {'display_name': 'New Name','acronym': 'NN'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        organization = Organization.objects.create(
            display_name='New Organization',
            acronym='NO',
            type=OrganizationType.objects.get(pk=1),
        )
        organization.territory.set([Territory.objects.get(pk=1)])
        response = self.client.put('/organizations/1/', {'display_name': 'New Name','acronym': 'NN'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.user.is_staff = True
        response = self.client.put('/organizations/1/', {'display_name': 'New Name','acronym': 'NN'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.is_staff = False
        organization.managers.set([self.user])
        response = self.client.put('/organizations/1/', {'display_name': 'Other New Name','acronym': 'ONN'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_org(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch('/organizations/1/', {'display_name': 'New Name'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        organization = Organization.objects.create(
            display_name='New Organization',
            acronym='NO',
            type=OrganizationType.objects.get(pk=1),
        )
        organization.territory.set([Territory.objects.get(pk=1)])
        response = self.client.patch('/organizations/1/', {'display_name': 'New Name'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.user.is_staff = True
        response = self.client.patch('/organizations/1/', {'display_name': 'New Name'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.user.is_staff = False
        organization.managers.set([self.user])
        response = self.client.patch('/organizations/1/', {'display_name': 'Other New Name'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class ListOrganizationsViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password=str(secrets.randbits(16)))
        self.client = APIClient()
        OrganizationType.objects.create(type_name='Type 1', type_code='TYPE1')
        Territory.objects.create(territory_name='Territory 1')

    def test_list_orgs_unauthenticated(self):
        response = self.client.get('/list_affiliation/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_orgs_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/list_affiliation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.create(
            display_name='New Organization',
            acronym='NO',
            type=OrganizationType.objects.get(pk=1),
        )
        organization.territory.set([Territory.objects.get(pk=1)])
        response = self.client.get('/list_affiliation/')
        self.assertEqual(len(response.data), 1)
        expected = {
            1: 'New Organization (NO)',
        }
        self.assertEqual(response.data, expected)

        Organization.objects.create(
            display_name='New Organization 2',
            acronym='NO2', 
            type=OrganizationType.objects.get(pk=1),
        )
        organization.territory.set([Territory.objects.get(pk=1)])
        organization.managers.set([self.user])
        response = self.client.get('/list_affiliation/')
        self.assertEqual(len(response.data), 2)
        expected = {
            1: 'New Organization (NO)',
            2: 'New Organization 2 (NO2)',
        }
        self.assertEqual(response.data, expected)

    def test_list_orgs_staff(self):
        self.user.is_staff = True
        self.client.force_authenticate(self.user)
        response = self.client.get('/list_affiliation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        org_data = {
            'display_name': 'New Organization',
            'acronym': 'NO',
            'type': '1',
            'territory': '1',
        }
        self.client.post('/organizations/', org_data)
        response = self.client.get('/list_affiliation/')
        self.assertEqual(len(response.data), 1)
