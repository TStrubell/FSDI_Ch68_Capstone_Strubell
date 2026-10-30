from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class RegistrationViewTests(TestCase):
    """Tests for SGnG user registration."""

    def setUp(self):
        self.register_url = reverse(
            "accounts:register"
        )

    def test_registration_page_returns_200(self):
        response = self.client.get(
            self.register_url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_registration_uses_correct_template(self):
        response = self.client.get(
            self.register_url
        )

        self.assertTemplateUsed(
            response,
            "registration/signup.html",
        )

    def test_registration_page_contains_heading(self):
        response = self.client.get(
            self.register_url
        )

        self.assertContains(
            response,
            "Create an Account",
        )

    def test_valid_registration_creates_user(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongTestPass123!",
            "password2": "StrongTestPass123!",
        }

        response = self.client.post(
            self.register_url,
            data=form_data,
        )

        self.assertEqual(
            User.objects.count(),
            1,
        )

        user = User.objects.get(
            username="testuser"
        )

        self.assertEqual(
            user.email,
            "test@example.com",
        )

        self.assertTrue(
            user.check_password(
                "StrongTestPass123!"
            )
        )

        self.assertRedirects(
            response,
            reverse("accounts:login"),
        )

    def test_mismatched_passwords_do_not_create_user(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongTestPass123!",
            "password2": "DifferentPass123!",
        }

        response = self.client.post(
            self.register_url,
            data=form_data,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            User.objects.count(),
            0,
        )


class LoginViewTests(TestCase):
    """Tests for SGnG login."""

    def setUp(self):
        self.login_url = reverse(
            "accounts:login"
        )

        self.user = User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="StrongTestPass123!",
        )

    def test_login_page_returns_200(self):
        response = self.client.get(
            self.login_url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_login_uses_correct_template(self):
        response = self.client.get(
            self.login_url
        )

        self.assertTemplateUsed(
            response,
            "registration/login.html",
        )

    def test_valid_login_redirects_home(self):
        response = self.client.post(
            self.login_url,
            data={
                "username": "loginuser",
                "password": "StrongTestPass123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("pages:home"),
        )

    def test_valid_login_authenticates_user(self):
        response = self.client.post(
            self.login_url,
            data={
                "username": "loginuser",
                "password": "StrongTestPass123!",
            },
        )

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

    def test_invalid_login_does_not_authenticate(self):
        response = self.client.post(
            self.login_url,
            data={
                "username": "loginuser",
                "password": "wrong-password",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )


class LogoutViewTests(TestCase):
    """Tests for SGnG logout."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="logoutuser",
            password="StrongTestPass123!",
        )

        self.client.force_login(
            self.user
        )

    def test_logout_post_redirects_home(self):
        response = self.client.post(
            reverse("accounts:logout")
        )

        self.assertRedirects(
            response,
            reverse("pages:home"),
        )

    def test_logout_removes_authentication(self):
        self.client.post(
            reverse("accounts:logout")
        )

        response = self.client.get(
            reverse("pages:home")
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )


class SuperuserTests(TestCase):
    """Tests administrative account flags."""

    def test_superuser_has_required_permissions(self):
        admin_user = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="StrongAdminPass123!",
        )

        self.assertTrue(
            admin_user.is_superuser
        )

        self.assertTrue(
            admin_user.is_staff
        )

        self.assertTrue(
            admin_user.is_active
        )