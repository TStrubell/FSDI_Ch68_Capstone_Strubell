from django.contrib.auth import (
    get_user_model,
)

from django.test import TestCase

from django.urls import reverse


User = get_user_model()


class AccountViewTests(TestCase):

    def setUp(self):
        self.password = (
            "StrongTestPassword123!"
        )

        self.user = (
            User.objects.create_user(
                username="existinguser",
                email="existing@example.com",
                password=self.password,
            )
        )

    def test_register_page_returns_200(self):
        response = self.client.get(
            reverse(
                "accounts:register"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_register_page_uses_template(self):
        response = self.client.get(
            reverse(
                "accounts:register"
            )
        )

        self.assertTemplateUsed(
            response,
            "registration/signup.html",
        )

    def test_registration_creates_user(self):
        response = self.client.post(
            reverse(
                "accounts:register"
            ),
            data={
                "username": "newuser",
                "email": "new@example.com",
                "password1": (
                    "StrongNewPassword123!"
                ),
                "password2": (
                    "StrongNewPassword123!"
                ),
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            User.objects.filter(
                username="newuser"
            ).exists()
        )

    def test_registration_redirects_to_login(self):
        response = self.client.post(
            reverse(
                "accounts:register"
            ),
            data={
                "username": "newuser",
                "email": "new@example.com",
                "password1": (
                    "StrongNewPassword123!"
                ),
                "password2": (
                    "StrongNewPassword123!"
                ),
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "accounts:login"
            ),
        )

    def test_login_page_returns_200(self):
        response = self.client.get(
            reverse(
                "accounts:login"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_valid_login_redirects_home(self):
        response = self.client.post(
            reverse(
                "accounts:login"
            ),
            data={
                "username": (
                    self.user.username
                ),
                "password": (
                    self.password
                ),
            },
        )

        self.assertRedirects(
            response,
            reverse("pages:home"),
        )

    def test_invalid_login_remains_on_page(self):
        response = self.client.post(
            reverse(
                "accounts:login"
            ),
            data={
                "username": (
                    self.user.username
                ),
                "password": (
                    "WrongPassword"
                ),
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )