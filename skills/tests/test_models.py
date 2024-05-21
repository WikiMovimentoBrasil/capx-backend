from django.test import TestCase
from django.utils import timezone
from skills.models import Skill

class SkillModelTest(TestCase):
    def test_skill_creation(self):
        skill = Skill.objects.create(
            skill_wikidata_item="Q123456789"
        )
        self.assertEqual(skill.skill_wikidata_item, "Q123456789")
        self.assertTrue(skill.skill_date_of_creation <= timezone.now())

    def test_skill_str(self):
        skill = Skill.objects.create(
            skill_wikidata_item="Q123456789"
        )
        self.assertEqual(str(skill), "Q123456789")
