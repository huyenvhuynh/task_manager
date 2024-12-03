# tests.py

from django.test import TestCase, Client, tag
from django.contrib.auth.models import User
from django.urls import reverse


@tag('homepage')
class HomepageTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_authenticated_navbar(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Simulate visiting the homepage
        response = self.client.get('/')

        # Check if the navbar for authenticated users is present
        self.assertContains(response, 'Your role:', status_code=200)

@tag('assignment_access')
class AssignmentAccessTest(TestCase):
    def test_authenticated_user_access(self):
        # Create a test user and log in
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Access the assignments page
        response = self.client.get(reverse('assignments:assignment_list'))
        # Check if the user gets a successful response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Assignments')

