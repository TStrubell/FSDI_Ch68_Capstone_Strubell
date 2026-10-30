from django.test import TestCase

from django.urls import reverse

from contact.forms import ContactForm


class ContactViewTests(TestCase):

    def setUp(self):

        self.url = reverse(
            "contact:contact"
        )

        self.valid_data = {
            "name": "Test User",

            "email": (
                "test@example.com"
            ),

            "subject": (
                "Marketplace inquiry"
            ),

            "message": (
                "I would like "
                "additional information "
                "about an SGnG product."
            ),
        }

    def test_page_returns_200(self):
        response = (
            self.client.get(
                self.url
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_correct_template(self):
        response = (
            self.client.get(
                self.url
            )
        )

        self.assertTemplateUsed(
            response,
            "contact/contact.html",
        )

    def test_form_in_context(self):
        response = (
            self.client.get(
                self.url
            )
        )

        self.assertIsInstance(
            response.context["form"],
            ContactForm,
        )

    def test_page_contains_heading(self):
        response = (
            self.client.get(
                self.url
            )
        )

        self.assertContains(
            response,
            "Contact SGnG",
        )

    def test_page_contains_send_button(self):
        response = (
            self.client.get(
                self.url
            )
        )

        self.assertContains(
            response,
            "Send Message",
        )

    def test_valid_submission_redirects(self):
        response = (
            self.client.post(
                self.url,
                data=self.valid_data,
            )
        )

        self.assertRedirects(
            response,
            self.url,
        )

    def test_success_message(self):
        response = (
            self.client.post(
                self.url,
                data=self.valid_data,
                follow=True,
            )
        )

        self.assertContains(
            response,
            (
                "Thank you for "
                "contacting SGnG. "
                "Your message was "
                "received successfully."
            ),
        )

    def test_invalid_email_returns_200(self):
        data = (
            self.valid_data.copy()
        )

        data["email"] = (
            "invalid-email"
        )

        response = (
            self.client.post(
                self.url,
                data=data,
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(
            "email",
            response
            .context["form"]
            .errors,
        )