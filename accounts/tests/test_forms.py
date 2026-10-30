from django.test import TestCase

from accounts.forms import SignUpForm


class SignUpFormTests(TestCase):

    def test_valid_signup_form(self):
        form = SignUpForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": (
                    "StrongTestPassword123!"
                ),
                "password2": (
                    "StrongTestPassword123!"
                ),
            }
        )

        self.assertTrue(
            form.is_valid()
        )

    def test_passwords_must_match(self):
        form = SignUpForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": (
                    "StrongTestPassword123!"
                ),
                "password2": (
                    "DifferentPassword123!"
                ),
            }
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "password2",
            form.errors,
        )

    def test_username_is_required(self):
        form = SignUpForm(
            data={
                "username": "",
                "email": "test@example.com",
                "password1": (
                    "StrongTestPassword123!"
                ),
                "password2": (
                    "StrongTestPassword123!"
                ),
            }
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "username",
            form.errors,
        )

    def test_duplicate_username_rejected(self):
        first_form = SignUpForm(
            data={
                "username": "testuser",
                "email": "one@example.com",
                "password1": (
                    "StrongTestPassword123!"
                ),
                "password2": (
                    "StrongTestPassword123!"
                ),
            }
        )

        self.assertTrue(
            first_form.is_valid()
        )

        first_form.save()

        duplicate_form = SignUpForm(
            data={
                "username": "testuser",
                "email": "two@example.com",
                "password1": (
                    "AnotherStrongPassword123!"
                ),
                "password2": (
                    "AnotherStrongPassword123!"
                ),
            }
        )

        self.assertFalse(
            duplicate_form.is_valid()
        )

        self.assertIn(
            "username",
            duplicate_form.errors,
        )