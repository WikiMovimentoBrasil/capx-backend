from django.test import TestCase
from django.urls import reverse
from ..models import CustomUser


class HomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_homepage_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view_url_accessible_by_name(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_view_uses_the_right_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/index.html")


class ProfileViewTest(TestCase):
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

    def test_profile_view_exists_as_an_unauthenticated_user(self):
        response = self.client.get(reverse('profile'))
        self.assertNotEqual(response.status_code, 200)

    def test_profile_view_status_code_as_an_authenticated_user(self):
        self.client.login(
            username="Abrahmovic",
            password= "Movic202310"
        )

        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)

    def test_profile_view_url_accessible_by_name_as_an_authenticated_user(self):
        self.client.login(
            username="Abrahmovic",
            password="Movic202310"
        )
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
    def test_profile_view_uses_correct_template_as_an_authenticated_user(self):
        self.client.login(
            username="Abrahmovic",
            password="Movic202310"
        )
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'users/profile.html')


class OAuthLoginViewTest(TestCase):
    def test_login_oauth_redirect(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        expected_url = reverse('social:begin', kwargs={"backend": "mediawiki"})
        self.assertEqual(response.url, expected_url)
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

class LogoutViewTest(TestCase):
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

    def test_logout_view(self):
        self.client.login(
            username="Abrahmovic",
            password="Movic202310"
        )
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))
        self.assertFalse('_auth_user_id' in self.client.session)



