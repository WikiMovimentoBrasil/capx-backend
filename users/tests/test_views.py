import profile
import secrets
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import Profile, CustomUser
from users.submodels import Territory, Language, WikimediaProject
from users.serializers import ProfileSerializer, TerritorySerializer, LanguageSerializer, WikimediaProjectSerializer
from skills.models import Skill
from orgs.models import Organization

class ProfileViewSetTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password=str(secrets.randbits(16)))
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
            'user': {},
            'about': 'first user ever!',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles.first())
        self.assertEqual(serializer.data['about'], updated_data['about'])

    def test_destroy_profile(self):
        response = self.client.delete('/profile/' + str(self.user.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_profile(self):
        response = self.client.post('/profile/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_other_profile(self):
        user = CustomUser.objects.create_user(username='test2', password=str(secrets.randbits(16)))
        self.assertNotEqual(user.pk, self.user.pk)

        url = '/profile/' + str(user.pk) + '/'
        updated_data = {
            'user': {},
            'about': 'second user ever!',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_unmatch_skills_profile(self):
        skill = Skill.objects.create(
            skill_wikidata_item="Q123456789"
        )

        url = '/profile/' + str(self.user.pk) + '/'
        updated_data = {
            'user': {},
            'skills_available': [str(skill.pk)],
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_update_match_skills_profile(self):
        skill = Skill.objects.create(
            skill_wikidata_item="Q123456789"
        )

        url = '/profile/' + str(self.user.pk) + '/'
        updated_data = {
            'user': {},
            'skills_known': [str(skill.pk)],
            'skills_available': [str(skill.pk)],
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_no_skill_provided(self):
        url = '/profile/' + str(self.user.pk) + '/'
        updated_data = {
            'user': {},
            'skills_known': [],
            'skills_available': [],
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_find_user_by_username(self):
        response = self.client.get('/users/?username=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        self.assertEqual(response.data, serializer.data)

class ListyViewSetTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password=str(secrets.randbits(16)))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_territories_list(self):
        Territory.objects.create(territory_name='test')
        Territory.objects.create(territory_name='test2')

        response = self.client.get('/list_territory/')
        territories = Territory.objects.all()
        expected_data = {territory.pk: territory.territory_name for territory in territories}
        self.assertEqual(response.data, expected_data)

    def test_get_languages_list(self):
        Language.objects.create(language_name='test', language_code='test')
        Language.objects.create(language_name='test2', language_code='test2')

        response = self.client.get('/list_language/')
        languages = Language.objects.all()
        expected_data = {language.pk: language.language_name for language in languages}
        self.assertEqual(response.data, expected_data)

    def test_get_wikimedia_projects_list(self):
        WikimediaProject.objects.create(wikimedia_project_name='test', wikimedia_project_code='test')
        WikimediaProject.objects.create(wikimedia_project_name='test2', wikimedia_project_code='test2')

        response = self.client.get('/list_wikimedia_project/')
        wikimedia_projects = WikimediaProject.objects.all()
        expected_data = {wikimedia_project.pk: wikimedia_project.wikimedia_project_name for wikimedia_project in wikimedia_projects}
        self.assertEqual(response.data, expected_data)

class UsersBySkillTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password=str(secrets.randbits(16)))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_users_by_skill(self):
        skill = Skill.objects.create(
            skill_wikidata_item="Q123456789"
        )
        profile = Profile.objects.get(user=self.user)
        profile.skills_known.add(skill)

        response = self.client.get('/users_by_skill/' + str(skill.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data['known']
        serializer_data = ProfileSerializer(Profile.objects.filter(skills_known=skill), many=True).data
        simplified_serializer_data = [
            {
                'id': profile['user']['id'],
                'display_name': profile['display_name'],
                'username': profile['user']['username'],
                'profile_image': profile['profile_image']
            } for profile in serializer_data
        ]
        self.assertEqual(response_data, simplified_serializer_data)
    
    def test_get_users_by_skill_no_id(self):
        response = self.client.get('/users_by_skill/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users_by_skill_not_found(self):
        response = self.client.get('/users_by_skill/0/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users_by_skill_no_users(self):
        skill = Skill.objects.create(
            skill_wikidata_item="Q123456789"
        )

        response = self.client.get('/users_by_skill/' + str(skill.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'known': [], 'available': [], 'wanted': []})

class UsersByTagTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password=str(secrets.randbits(16)))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_users_by_tag_no_tag_type(self):
        response = self.client.get('/tags/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users_by_tag_skill(self):
        skill = Skill.objects.create(
            skill_wikidata_item="Q123456789"
        )
        profile = Profile.objects.get(user=self.user)
        profile.skills_known.add(skill)

        response = self.client.get('/tags/skill/' + str(skill.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data['known']
        serializer_data = ProfileSerializer(Profile.objects.filter(skills_known=skill), many=True).data
        simplified_serializer_data = [
            {
                'id': profile['user']['id'],
                'display_name': profile['display_name'],
                'username': profile['user']['username'],
                'profile_image': profile['profile_image']
            } for profile in serializer_data
        ]
        self.assertEqual(response_data, simplified_serializer_data)

    def test_get_users_by_tag_skill_no_id(self):
        response = self.client.get('/tags/skill/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users_by_tag_skill_not_found(self):
        response = self.client.get('/tags/skill/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users_by_tag_skill_no_users(self):
        skill = Skill.objects.create(
            skill_wikidata_item="Q123456789"
        )

        response = self.client.get('/tags/skill/' + str(skill.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'known': [], 'available': [], 'wanted': []})

    def test_get_users_by_tag_language(self):
        language = Language.objects.create(
            language_name='test',
            language_code='test'
        )
        profile = Profile.objects.get(user=self.user)
        profile.language.set([language])

        response = self.client.get('/tags/language/' + str(language.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        serializer_data = ProfileSerializer(Profile.objects.filter(language=language), many=True).data
        simplified_serializer_data = [
            {
                'id': profile['user']['id'],
                'display_name': profile['display_name'],
                'username': profile['user']['username'],
                'profile_image': profile['profile_image']
            } for profile in serializer_data
        ]
        self.assertEqual(response_data, simplified_serializer_data)

    def test_get_users_by_tag_language_no_id(self):
        response = self.client.get('/tags/language/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users_by_tag_language_not_found(self):
        response = self.client.get('/tags/language/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users_by_tag_language_no_users(self):
        language = Language.objects.create(
            language_name='test',
            language_code='test'
        )

        response = self.client.get('/tags/language/' + str(language.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_users_by_tag_territory(self):
        territory = Territory.objects.create(
            territory_name='test'
        )
        profile = Profile.objects.get(user=self.user)
        profile.territory.set([territory])

        response = self.client.get('/tags/territory/' + str(territory.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        serializer_data = ProfileSerializer(Profile.objects.filter(territory=territory), many=True).data
        simplified_serializer_data = [
            {
                'id': profile['user']['id'],
                'display_name': profile['display_name'],
                'username': profile['user']['username'],
                'profile_image': profile['profile_image']
            } for profile in serializer_data
        ]
        self.assertEqual(response_data, simplified_serializer_data)

    def test_get_users_by_tag_territory_no_id(self):
        response = self.client.get('/tags/territory/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users_by_tag_territory_not_found(self):
        response = self.client.get('/tags/territory/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users_by_tag_territory_no_users(self):
        territory = Territory.objects.create(
            territory_name='test'
        )

        response = self.client.get('/tags/territory/' + str(territory.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
    
    def test_get_users_by_tag_wikimedia_project(self):
        wikimedia_project = WikimediaProject.objects.create(
            wikimedia_project_name='test',
            wikimedia_project_code='test'
        )
        profile = Profile.objects.get(user=self.user)
        profile.wikimedia_project.set([wikimedia_project])

        response = self.client.get('/tags/wikimedia_project/' + str(wikimedia_project.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        serializer_data = ProfileSerializer(Profile.objects.filter(wikimedia_project=wikimedia_project), many=True).data
        simplified_serializer_data = [
            {
                'id': profile['user']['id'],
                'display_name': profile['display_name'],
                'username': profile['user']['username'],
                'profile_image': profile['profile_image']
            } for profile in serializer_data
        ]
        self.assertEqual(response_data, simplified_serializer_data)

    def test_get_users_by_tag_wikimedia_project_no_id(self):
        response = self.client.get('/tags/wikimedia_project/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_users_by_tag_wikimedia_project_not_found(self):
        response = self.client.get('/tags/wikimedia_project/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users_by_tag_wikimedia_project_no_users(self):
        wikimedia_project = WikimediaProject.objects.create(
            wikimedia_project_name='test',
            wikimedia_project_code='test'
        )

        response = self.client.get('/tags/wikimedia_project/' + str(wikimedia_project.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_users_by_tag_invalid_tag_type(self):
        response = self.client.get('/tags/invalid/1/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_users_by_tag_invalid_tag_id(self):
        response = self.client.get('/tags/skill/invalid/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users_by_tag_affiliation(self):
        organization = Organization.objects.create(
            display_name='New Organization',
            acronym='NO'
        )
        profile = Profile.objects.get(user=self.user)
        profile.affiliation.set([organization])

        response = self.client.get('/tags/affiliation/' + str(organization.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        serializer_data = ProfileSerializer(Profile.objects.filter(affiliation=organization), many=True).data
        simplified_serializer_data = [
            {
                'id': profile['user']['id'],
                'display_name': profile['display_name'],
                'username': profile['user']['username'],
                'profile_image': profile['profile_image']
            } for profile in serializer_data
        ]
        self.assertEqual(response_data, simplified_serializer_data)    
