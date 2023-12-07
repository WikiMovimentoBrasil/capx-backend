from django.test import TestCase
from django.db import IntegrityError
from .models import Region, Language, WikimediaProject, AreaOfInterest, Organization

# Create your tests here.

# models test


class RegionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region = Region.objects.create(
            region_name = "Africa",
            # parent_region = "",

        )

    def test_region_model(self):
        self.assertEqual(self.region.region_name, "Africa")
        self.assertEqual(str(self.region), "Africa")

    def test_uniqueness_region_name(self):
        Region.objects.create(region_name="Asia")
        with self.assertRaises(IntegrityError):
            Region.objects.create(region_name="Asia")


class LanguageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.language = Language.objects.create(
            language_name="Spanish",
            language_code="es"
        )

    def test_language_model(self):
        self.assertEqual(self.language.language_name, "Spanish")
        self.assertEqual(self.language.language_code, "es")
        self.assertEqual(str(self.language), "Spanish")

    def test_unique_language_code(self):
        # Test that language_code is unique
        Language.objects.create(language_name="Spanish", language_code="es")
        with self.assertRaises(IntegrityError):
            Language.objects.create(language_name="Hausa", language_code="es")


class WikimediaProjectTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.wikimedia_project = WikimediaProject.objects.create(
            wikimedia_project_name="Wikipedia",
            wikimedia_project_code="wiki"
        )

    def test_wikimedia_project(self):
        self.assertEqual(self.wikimedia_project.wikimedia_project_name, "Wikipedia")
        self.assertEqual(self.wikimedia_project.wikimedia_project_code, "wiki")
        self.assertEqual(str(self.wikimedia_project), "Wikipedia")

    def test_unique_wikimedia_project_code(self):
        # Test that language_code is unique
        WikimediaProject.objects.create(wikimedia_project_name="Wikimedia Commons", wikimedia_project_code="wiki")
        with self.assertRaises(IntegrityError):
            WikimediaProject.objects.create(wikimedia_project_name="Wikidata", wikimedia_project_code="wiki")


class AreaOfInterestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.area_of_interest = AreaOfInterest.objects.create(
            area_name="Diversity"
        )

    def test_area_of_interest_model(self):
        self.assertEqual(self.area_of_interest.area_name, "Diversity")
        self.assertEqual(str(self.area_of_interest), "Diversity")


class OrganizationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = Organization.objects.create(
            type_code="",
            type_name=""
        )
