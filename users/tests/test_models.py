from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from ..models import Region, Language, WikimediaProject, Organization, CustomUser, \
    Profile

# TODO: Add the tests for the skills relationship with the profile model


class RegionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.parent_region = Region.objects.create(
            region_name="Africa",
        )
        cls.region = Region.objects.create(
            region_name="Nigeria",

        )
        cls.region.parent_region.set([cls.parent_region])
        # cls.region.parent_region.set(1])

    def test_region_creation(self):
        self.assertEqual(self.region.region_name, "Nigeria")
        self.assertEqual(str(self.region), "Nigeria")

        self.assertIn(self.parent_region, self.region.parent_region.all())

    def test_unique_region_name(self):
        Region.objects.create(region_name="Asia")
        with self.assertRaises(IntegrityError):
            Region.objects.create(region_name="Asia")


class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.language = Language.objects.create(
            language_name="Spanish",
            language_code="es"
        )

    def test_language_model_creation(self):
        self.assertEqual(self.language.language_name, "Spanish")
        self.assertEqual(self.language.language_code, "es")
        self.assertEqual(str(self.language), "Spanish")

    def test_unique_language_code(self):
        # Test that language_code is unique
        Language.objects.create(language_name="English", language_code="en")
        with self.assertRaises(IntegrityError):
            Language.objects.create(language_name="Hausa", language_code="en")


class WikimediaProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.wikimedia_project = WikimediaProject.objects.create(
            wikimedia_project_name="Wikipedia",
            wikimedia_project_code="wiki"
        )

    def test_wikimedia_project_creation(self):
        self.assertEqual(self.wikimedia_project.wikimedia_project_name, "Wikipedia")
        self.assertEqual(self.wikimedia_project.wikimedia_project_code, "wiki")
        self.assertEqual(str(self.wikimedia_project), "Wikipedia")

    def test_unique_wikimedia_project_code(self):
        WikimediaProject.objects.create(wikimedia_project_name="Wikimedia Commons", wikimedia_project_code="commonswiki")
        with self.assertRaises(IntegrityError):
            WikimediaProject.objects.create(wikimedia_project_name="Wikidata", wikimedia_project_code="commonswiki")


class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects._create_user(
            username="Abrahmovic",
            email="abrahmovic@hot.com",
            password="Movic202310",
            first_name="Abrah",
            middle_name="Omo",
            last_name="Movic",
        )

    def test_custom_user_creation(self):
        self.assertEqual(self.user.username, "Abrahmovic")
        self.assertEqual(self.user.email, "abrahmovic@hot.com")

    def test_username_uniqueness(self):
        # Test the uniqueness of the username
        with self.assertRaises(IntegrityError):
            another_user = CustomUser.objects.create_user(
                username="Abrahmovic",
                email="another@example.com",
                password="Movic202310",
            )
            another_user.full_clean()


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region = Region.objects.create(
            region_name="Canada",
        )
        cls.language = Language.objects.create(
            language_name="French",
            language_code="fr"
        )

        cls.wikimedia_project = WikimediaProject.objects.create(
            wikimedia_project_name="Wikipedia",
            wikimedia_project_code="wiki"
        )
        cls.user = CustomUser.objects._create_user(
            username="Abrahmovic",
            email="abrahmovic@hot.com",
            password="Movic202310",
            first_name="Abrah",
            middle_name="Omo",
            last_name="Movic",
        )

    def test_profile_creation(self):
        self.assertIsNotNone(self.user.profile)
        self.assertEqual(self.user.profile.user, self.user)

    def test_profile_fields(self):
        # Test filling in various fields of Profile
        profile = self.user.profile
        profile.pronoun = 'he-him'
        profile.contact_method = "wiki"
        profile.display_name = 'AbrahmotheBaller'
        profile.save()

        updated_profile = Profile.objects.get(id=profile.id)
        self.assertEqual(updated_profile.pronoun, 'he-him')
        self.assertEqual(updated_profile.display_name, 'AbrahmotheBaller')

    def test_invalid_pronoun_validation(self):
        profile = self.user.profile
        profile.pronoun = 'invalid_pronoun'
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_localization(self):
        profile = self.user.profile
        profile.region.set([self.region])
        profile.language.set([self.language])
        profile.wikimedia_project.set([self.wikimedia_project])
        profile.save()

        updated_profile = Profile.objects.get(id=profile.id)
        region = [region.region_name for region in updated_profile.region.all()]
        language = [language.language_name for language in updated_profile.language.all()]
        affiliation = [organization.organization_name for organization in updated_profile.affiliation.all()]
        wikimedia_project = [wikimedia_project.wikimedia_project_name for wikimedia_project in
                             updated_profile.wikimedia_project.all()]

        self.assertIn('Canada', region)
        self.assertIn("French", language)
        self.assertIn("Wikimedia Canada", affiliation)
        self.assertIn("Wikipedia", wikimedia_project)
        self.assertIn("Diversity", area_of_interest)

    def test_profile_str_method_with_full_name(self):
        user = CustomUser.objects.create_user(
            username="Andy",
            first_name="Andrew",
            middle_name="Jay",
            last_name="Nicole",
            email="andy@wiki.com",
            password="WIkiWikiAn34"
        )

        self.assertEqual(str(user.profile), "Andrew J. Nicole")

    def test_profile_str_method_with_first_and_last_name(self):
        user = CustomUser.objects.create_user(
            username="Angela",
            first_name="Angela",
            last_name="Brown",
            email="ab@wemia.com",
            password="WemB2840"
        )

        self.assertEqual(str(user.profile), "Angela Brown")

    def test_profile_str_method_with_first_name(self):
        user = CustomUser.objects.create_user(
            username="Ali",
            first_name="Alice",
        )

        self.assertEqual(str(user.profile), "Alice")

    def test_profile_str_method_with_only_username(self):
        user = CustomUser.objects.create_user(
            username="Anthony",
        )
        self.assertEqual(str(user.profile), "Anthony")
