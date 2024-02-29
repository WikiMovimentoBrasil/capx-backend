from django.test import TestCase
from django.urls import reverse
from ..models import Bug, Attachment
from users.models import CustomUser


class HomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.test_user.save()

    def setUp(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

    def test_homepage_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view_url_accessible_by_name(self):
        response = self.client.get(reverse("bugs:homepage"))
        self.assertNotEqual(response.status_code, 200)

    def test_homepage_view_uses_the_right_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse("bugs:homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bugs/bug_list.html")


class BugFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.test_user.save()

    def setUp(self):
        # Log in the test user
        self.client.login(username='testuser', password='12345')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("bugs:register_bug"))
        expected_url = f'/login/?next={reverse("bugs:register_bug")}'
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)
        self.assertNotEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse("bugs:register_bug"))
        # response = self.client.get(self.bug_form_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("bugs:register_bug"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bugs/register_bug.html')

    def test_successful_form_submission(self):
        response = self.client.post(reverse("bugs:register_bug"), {'title': 'Test Bug', 'description': 'Just a test'})
        self.assertEqual(Bug.objects.count(), 1)
        self.assertRedirects(response, reverse('bugs:homepage'))

    def test_form_errors_for_invalid_data(self):
        response = self.client.post(reverse("bugs:register_bug"), {})
        self.assertFormError(response, 'form', 'title', 'This field is required.')


class BugListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users, one regular and one superuser
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.superuser = CustomUser.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')
        # Create bugs for each user
        Bug.objects.create(title="User Bug", description="A bug by a regular user", user=cls.user)
        Bug.objects.create(title="Admin Bug", description="A bug by an admin", user=cls.superuser)

    def test_redirect_if_not_logged_in(self):
        # Ensure unauthenticated users are redirected to login
        response = self.client.get(reverse('bugs:bug_list'))
        expected_url = f'/login/?next={reverse("bugs:bug_list")}'
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_logged_in_user_sees_own_bugs(self):
        # Log in as a regular user
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('bugs:bug_list'))
        # Check that the user sees only their bugs
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bugs' in response.context)
        self.assertEqual(len(response.context['bugs']), 1)
        self.assertEqual(response.context['bugs'][0].user, self.user)

    def test_superuser_sees_all_bugs(self):
        # Log in as a superuser
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('bugs:bug_list'))
        # Check that the superuser sees all bugs
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bugs' in response.context)
        self.assertEqual(len(response.context['bugs']), 2)


class BugDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        # Create a test bug
        cls.bug = Bug.objects.create(title="Test Bug", description="A test bug.", user=cls.user)
        # Optionally, create an attachment for the bug
        # Attachment.objects.create(bug=cls.bug, file=<YourFileHere>)

    def setUp(self):
        # Log in the test user
        self.client.login(username='testuser', password='12345')

    def test_bug_detail_view_with_authenticated_user(self):
        # Access the bug detail page
        response = self.client.get(reverse('bug_detail', kwargs={'bug_id': self.bug.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bug.title)
        # If you're testing attachments, also check for attachment data
        # self.assertContains(response, <expected attachment detail>)

    def test_bug_detail_view_with_invalid_bug_id(self):
        # Access the bug detail page with an invalid bug ID
        response = self.client.get(reverse('bug_detail', kwargs={'bug_id': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_not_logged_in(self):
        # Log out the user
        self.client.logout()
        # Try to access the bug detail page
        response = self.client.get(reverse('bug_detail', kwargs={'bug_id': self.bug.pk}))
        self.assertRedirects(response, f'/login/?next={reverse("bug_detail", kwargs={"bug_id": self.bug.pk})}', fetch_redirect_response=False)