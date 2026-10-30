from django.test import SimpleTestCase

from contact.forms import ContactForm


class ContactFormTests(
    SimpleTestCase
):

    def setUp(self):
        self.valid_data = {
            "name": "Test User",

            "email": (
                "test@example.com"
            ),

            "subject": (
                "Marketplace inquiry"
            ),

            "message": (
                "I would like more "
                "information about "
                "an SGnG product."
            ),
        }

    def test_valid_form(self):
        form = ContactForm(
            data=self.valid_data
        )

        self.assertTrue(
            form.is_valid()
        )

    def test_name_required(self):
        data = (
            self.valid_data.copy()
        )

        data["name"] = ""

        form = ContactForm(
            data=data
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "name",
            form.errors,
        )

    def test_email_required(self):
        data = (
            self.valid_data.copy()
        )

        data["email"] = ""

        form = ContactForm(
            data=data
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "email",
            form.errors,
        )

    def test_email_must_be_valid(self):
        data = (
            self.valid_data.copy()
        )

        data["email"] = (
            "invalid-email"
        )

        form = ContactForm(
            data=data
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "email",
            form.errors,
        )

    def test_subject_required(self):
        data = (
            self.valid_data.copy()
        )

        data["subject"] = ""

        form = ContactForm(
            data=data
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "subject",
            form.errors,
        )

    def test_message_required(self):
        data = (
            self.valid_data.copy()
        )

        data["message"] = ""

        form = ContactForm(
            data=data
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "message",
            form.errors,
        )

    def test_message_placeholder(self):
        form = ContactForm()

        placeholder = (
            form
            .fields["message"]
            .widget
            .attrs
            .get("placeholder")
        )

        self.assertEqual(
            placeholder,
            (
                "Tell us about your "
                "question or "
                "marketplace inquiry."
            ),
        )