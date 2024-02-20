from django.test import TestCase
from django.urls import reverse
from skills.models import Skill


class SkillModelTest(TestCase):
    def test_skill_create(self):
        skill = Skill.objects.create(
            skill_name='Test Skill',
            skill_description='Description for Test Skill',
        )
        self.assertEqual(skill.skill_name, 'Test Skill')
        self.assertEqual(skill.skill_description, 'Description for Test Skill')


class SkillViewsTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            skill_name='Test Skill',
            skill_description='Description for Test Skill',
        )
        self.skill_update_data = {
            'skill_name': 'Updated Skill',
            'skill_description': 'Updated Description',
            'skill_type': [],
            'skill_wikidata_item': 'Q12345',
        }

    def test_skill__str__returns_skill_name_field(self):
        self.assertEqual(self.skill.__str__(),self.skill.skill_name)

    def test_skill_list_view(self):
        response = self.client.get(reverse('skill_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Skill')

    def test_skill_detail_view(self):
        response = self.client.get(reverse('skill_view', args=[self.skill.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Skill')

    def test_skill_create_view(self):
        response = self.client.post(reverse('skill_new'), data={
            'skill_name': 'New Skill',
            'skill_description': 'Description for New Skill',
            'skill_type': [],
            'skill_wikidata_item': 'Q54321',
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Skill.objects.filter(skill_name='New Skill').exists())

    def test_skill_update_view(self):
        response = self.client.post(reverse('skill_edit', args=[self.skill.id]), data=self.skill_update_data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        updated_skill = Skill.objects.get(id=self.skill.id)
        self.assertEqual(updated_skill.skill_name, 'Updated Skill')
        self.assertEqual(updated_skill.skill_wikidata_item, 'Q12345')

    def test_skill_delete_view(self):
        response = self.client.post(reverse('skill_delete', args=[self.skill.id]))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertFalse(Skill.objects.filter(id=self.skill.id).exists())