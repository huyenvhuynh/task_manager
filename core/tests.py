from django.conf import settings
from django.test import TestCase, tag

@tag('https')
class HttpsSettingsTest(TestCase):
    def test_https_settings(self):
        self.assertTrue(
            settings.SECURE_SSL_REDIRECT,
            "SECURE_SSL_REDIRECT should be enabled in production settings."
        )
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
            "SECURE_HSTS_PRELOAD should be enabled in production settings."
        )
        self.assertEqual(
            settings.SECURE_PROXY_SSL_HEADER, ('HTTP_X_FORWARDED_PROTO', 'https'),
            "SECURE_PROXY_SSL_HEADER should be configured for HTTPS."
        )
