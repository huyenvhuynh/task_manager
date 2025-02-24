from django.test import TestCase, tag
from django.urls import reverse

@tag('login')
class CustomLoginPageTest(TestCase):
    def test_custom_login_page_contains_elements(self):
        # Get the custom login page
        response = self.client.get(reverse('users:sign_in'))

        # Check if the page loads successfully
        self.assertEqual(response.status_code, 200, "Login page should load successfully.")

        # Check for the presence of Google Sign-In onload script using id attribute
        self.assertIn(
            'id="g_id_onload"', response.content.decode(),
            "The page should include the Google Sign-In onload script."
        )

        # Check for the Google Sign-In button
        self.assertIn(
            'class="g_id_signin"', response.content.decode(),
            "The page should include the Google Sign-In button."
        )

        # Check for the 'Continue without signing in' button text
        self.assertIn(
            'Continue without signing in', response.content.decode(),
            "The page should include a 'Continue without signing in' button."
        )
