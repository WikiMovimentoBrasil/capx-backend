from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import CustomUser
from skills.models import Skill
from skills.serializers import SkillSerializer

class SkillViewSetTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password='123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        skill = {
            'skill_name': "Programming",
            'skill_description': "A skill for writing code",
            'skill_wikidata_item': "Q123456789"
        }
        self.client.post('/skill/', skill)

    def test_get_skills_list(self):
        response = self.client.get('/skill/')
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_skill_detail(self):
        response = self.client.get('/skill/1/')
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills.first())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_skill(self):
        skill = {
            'skill_name': "Cooking",
            'skill_description': "A skill for cooking food",
            'skill_wikidata_item': "Q987654321"
        }
        response = self.client.post('/skill/', skill)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        skill = Skill.objects.get(skill_name='Cooking')
        serializer = SkillSerializer(skill)
        self.assertEqual(response.data, serializer.data)

    def test_update_skill(self):
        skill = Skill.objects.get(skill_name='Programming')
        updated_data = {
            'skill_name': 'Updated Skill',
        }
        response = self.client.patch('/skill/' + str(skill.pk) + '/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        skill.refresh_from_db()
        serializer = SkillSerializer(skill)
        self.assertEqual(serializer.data['skill_name'], updated_data['skill_name'])

    def test_delete_skill(self):
        response = self.client.delete('/skill/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)