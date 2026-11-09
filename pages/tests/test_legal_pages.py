from django.test import TestCase
from django.urls import reverse


class LegalPageTests(TestCase):
    def test_terms_of_service_url_resolves(self):
        url = reverse("pages:terms_of_service")

        self.assertEqual(url, "/terms-of-service/")

    def test_terms_of_service_page_returns_200(self):
        response = self.client.get(
            reverse("pages:terms_of_service")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "pages/terms_of_service.html",
        )

    def test_privacy_policy_url_resolves(self):
        url = reverse("pages:privacy_policy")

        self.assertEqual(url, "/privacy-policy/")

    def test_privacy_policy_page_returns_200(self):
        response = self.client.get(
            reverse("pages:privacy_policy")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "pages/privacy_policy.html",
        )