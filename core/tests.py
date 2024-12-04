from django.conf import settings
from django.test import TestCase, override_settings, tag

@tag('https')
class HttpsSettingsTest(TestCase):
    @override_settings(
        DEBUG=False,
        SECURE_SSL_REDIRECT=True,  # Explicitly set this for the test
        SECURE_HSTS_SECONDS=31536000,
        SECURE_HSTS_INCLUDE_SUBDOMAINS=True,
        SECURE_HSTS_PRELOAD=True
    )
    def test_https_settings(self):
        # Test HSTS settings
        self.assertEqual(
            settings.SECURE_HSTS_SECONDS, 31536000,
            "SECURE_HSTS_SECONDS should be set to 1 year in production."
        )
        self.assertTrue(
            settings.SECURE_HSTS_INCLUDE_SUBDOMAINS,
            "SECURE_HSTS_INCLUDE_SUBDOMAINS should be True in production."
        )
        self.assertTrue(
            settings.SECURE_HSTS_PRELOAD,
            "SECURE_HSTS_PRELOAD should be enabled in production."
        )

        # Test SSL Redirect
        self.assertTrue(
            settings.SECURE_SSL_REDIRECT,
            "SECURE_SSL_REDIRECT should be enabled in production settings."
        )

    @override_settings(
        DEBUG=True,
        SECURE_SSL_REDIRECT=False
    )
    def test_https_settings_debug(self):
        # Test SSL Redirect in non-production
        self.assertFalse(
            settings.SECURE_SSL_REDIRECT,
            "SECURE_SSL_REDIRECT should be disabled in non-production settings."
        )

@tag('workflow')
class GithubActionsTest(TestCase):
    @override_settings(
        GOOGLE_OAUTH_CLIENT_ID="test_client_id",
        GOOGLE_OAUTH_CLIENT_SECRET="test_client_secret"
    )
    def test_github_actions_env_variables(self):
        # Test environment variables
        self.assertEqual(
            settings.GOOGLE_OAUTH_CLIENT_ID, "test_client_id",
            "GOOGLE_OAUTH_CLIENT_ID should be correctly set in the GitHub Actions environment."
        )
        self.assertEqual(
            settings.GOOGLE_OAUTH_CLIENT_SECRET, "test_client_secret",
            "GOOGLE_OAUTH_CLIENT_SECRET should be correctly set in the GitHub Actions environment."
        )

        # Test DJANGO_SETTINGS_MODULE from environment variables
        import os
        self.assertEqual(
            os.environ.get("DJANGO_SETTINGS_MODULE"), "core.settings",
            "DJANGO_SETTINGS_MODULE should be set to 'core.settings'."
        )
