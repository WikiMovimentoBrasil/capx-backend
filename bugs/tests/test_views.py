from django.test import TestCase
from django.urls import reverse
from ..models import Bug, Attachment
from users.models import CustomUser


class HomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUser.objects.create_user(username='testuser', password='12345')
        test_user.save()

    def setUp(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

    def test_homepage_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view_url_accessible_by_name(self):
        response = self.client.get(reverse("bugs:homepage"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_view_uses_the_right_template(self):
        response = self.client.get(reverse("bugs:homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bugs/bug_list.html")


class BugFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUser.objects.create_user(username='testuser', password='12345')
        test_user.save()

    def setUp(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.bug_form_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.bug_form_url}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.bug_form_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.bug_form_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bugs/register_bug.html')

    def test_successful_form_submission(self):
        response = self.client.post(self.bug_form_url, {'title': 'Test Bug', 'description': 'Just a test'})
        self.assertEqual(Bug.objects.count(), 1)
        self.assertRedirects(response, reverse('bugs:homepage'))
        self.assertEqual(str(messages[0]), 'Bug submitted successfully!')

    def test_form_errors_for_invalid_data(self):
        response = self.client.post(self.bug_form_url, {})
        self.assertFormError(response, 'form', 'title', 'This field is required.')

