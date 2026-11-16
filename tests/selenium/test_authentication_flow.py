from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SeleniumTestCase


User = get_user_model()


class AuthenticationFlowTests(SeleniumTestCase):
    """
    Browser-level tests for SGnG user registration, login,
    and logout workflows.
    """

    TEST_PASSWORD = "SecureTestPassword123!"

    REGISTER_SUBMIT = (
        By.CSS_SELECTOR,
        'button[type="submit"]',
    )

    LOGIN_SUBMIT = (
        By.CSS_SELECTOR,
        'button[type="submit"]',
    )

    LOGOUT_BUTTON = (
        By.CSS_SELECTOR,
        ".nav-logout-button",
    )

    LOGIN_LINK = (
        By.CSS_SELECTOR,
        'a[href="/accounts/login/"]',
    )

    def test_user_registration(self):
        """
        Verify that a visitor can submit a valid registration form,
        create a Django user record, and reach the login page.
        """
        self.open("/accounts/register/")

        username_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "username",
                )
            )
        )

        email_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "email",
                )
            )
        )

        password1_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "password1",
                )
            )
        )

        password2_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "password2",
                )
            )
        )

        username_field.clear()
        username_field.send_keys(
            "seleniumuser"
        )

        email_field.clear()
        email_field.send_keys(
            "selenium@example.com"
        )

        password1_field.clear()
        password1_field.send_keys(
            self.TEST_PASSWORD
        )

        password2_field.clear()
        password2_field.send_keys(
            self.TEST_PASSWORD
        )

        self.safe_click(
            self.REGISTER_SUBMIT
        )

        self.wait.until(
            EC.url_contains(
                "/accounts/login/"
            )
        )

        self.wait_for_document_ready()

        self.assertTrue(
            User.objects.filter(
                username="seleniumuser"
            ).exists()
        )

    def test_user_login(self):
        """
        Verify that a registered user can log in successfully
        and reach the SGnG Home page.
        """
        User.objects.create_user(
            username="testcustomer",
            email="customer@example.com",
            password=self.TEST_PASSWORD,
        )

        self.open("/accounts/login/")

        username_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "username",
                )
            )
        )

        password_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "password",
                )
            )
        )

        username_field.clear()
        username_field.send_keys(
            "testcustomer"
        )

        password_field.clear()
        password_field.send_keys(
            self.TEST_PASSWORD
        )

        self.safe_click(
            self.LOGIN_SUBMIT
        )

        self.wait.until(
            EC.url_to_be(
                f"{self.live_server_url}/"
            )
        )

        self.wait_for_document_ready()

        self.wait.until(
            EC.visibility_of_element_located(
                self.LOGOUT_BUTTON
            )
        )

        self.assert_page_contains(
            "Logout"
        )

    def test_user_logout(self):
        """
        Verify that an authenticated user can log out and that
        the navigation returns to its anonymous-user state.
        """
        User.objects.create_user(
            username="logoutuser",
            email="logout@example.com",
            password=self.TEST_PASSWORD,
        )

        self.open("/accounts/login/")

        username_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "username",
                )
            )
        )

        password_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "password",
                )
            )
        )

        username_field.clear()
        username_field.send_keys(
            "logoutuser"
        )

        password_field.clear()
        password_field.send_keys(
            self.TEST_PASSWORD
        )

        self.safe_click(
            self.LOGIN_SUBMIT
        )

        self.wait.until(
            EC.url_to_be(
                f"{self.live_server_url}/"
            )
        )

        self.wait_for_document_ready()

        self.wait.until(
            EC.visibility_of_element_located(
                self.LOGOUT_BUTTON
            )
        )

        self.safe_click(
            self.LOGOUT_BUTTON
        )

        self.wait.until(
            EC.url_to_be(
                f"{self.live_server_url}/"
            )
        )

        self.wait_for_document_ready()

        self.wait.until(
            EC.invisibility_of_element_located(
                self.LOGOUT_BUTTON
            )
        )

        login_link = self.wait.until(
            EC.visibility_of_element_located(
                self.LOGIN_LINK
            )
        )

        self.assertTrue(
            login_link.is_displayed()
        )

        self.assertEqual(
            login_link.text.strip(),
            "Login",
        )
        