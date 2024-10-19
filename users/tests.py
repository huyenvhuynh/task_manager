from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from unittest.mock import patch
from users.models import Profile
import os

# Create your tests here.

# This tests the GitHub issue 'General Login #1', 'Django Admin Login #2'
class UserAuthentificationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.google_client_id = 'test-client-id'
        os.environ['GOOGLE_OAUTH_CLIENT_ID'] = self.google_client_id

        # Create a test user inside the setUp method
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            email='testuser@example.com'
        )
        # Create a profile with a role for the user
        self.user.profile.role = 'user'
        self.user.profile.save()
        
    def test_google_sign_in_view(self):
        # Testing that google_sign_in view returns the Google client ID
        response = self.client.get(reverse('users:google_sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.google_client_id)
        self.assertTemplateUsed(response, 'users/sign_in.html')

    def test_sign_in_view_authenticated_user(self):
        # Testing that an authenticated user is shown a success message
        self.client.login(username='testuser@example.com', password='password')
        response = self.client.get(reverse('users:sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Successfully signed in as a Common User!')
        self.assertTemplateUsed(response, 'users/sign_in.html')

    def test_sign_in_view_unauthenticated_user(self):
        # Testing that an unauthenticated user is shown the sign-in page with the Google client ID
        response = self.client.get(reverse('users:sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.google_client_id)
        self.assertTemplateUsed(response, 'users/sign_in.html')
    
    def test_select_role_view_get(self):
        # Test that the select_role view returns the correct template for GET requests.
        self.client.login(username='testuser@example.com', password='password')
        response = self.client.get(reverse('users:select_role'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/select_role.html')

    def test_select_role_view_post_valid_role(self):
        # Test that a valid role is saved and the user is redirected with a success message."""
        self.client.login(username='testuser@example.com', password='password')
        response = self.client.post(reverse('users:select_role'), {'role': 'admin'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Successfully signed in as an Administrator!')

        # Session data is cleared
        self.assertNotIn('_auth_user_id', self.client.session)


