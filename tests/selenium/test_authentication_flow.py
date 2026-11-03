from django.contrib.auth import get_user_model

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SeleniumTestCase


User = get_user_model()


class AuthenticationFlowTests(SeleniumTestCase):
    """
    Browser-level tests for Register, Login, and Logout.
    """

    def test_user_registration(self):
        self.open("/accounts/register/")

        username = self.browser.find_element(
            By.NAME,
            "username",
        )

        email = self.browser.find_element(
            By.NAME,
            "email",
        )

        password1 = self.browser.find_element(
            By.NAME,
            "password1",
        )

        password2 = self.browser.find_element(
            By.NAME,
            "password2",
        )

        username.send_keys(
            "seleniumuser"
        )

        email.send_keys(
            "selenium@example.com"
        )

        password1.send_keys(
            "SecureTestPassword123!"
        )

        password2.send_keys(
            "SecureTestPassword123!"
        )

        self.browser.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]',
        ).click()

        self.wait.until(
            EC.url_contains(
                "/accounts/login/"
            )
        )

        self.assertTrue(
            User.objects.filter(
                username="seleniumuser"
            ).exists()
        )


    def test_user_login(self):
        User.objects.create_user(
            username="testcustomer",
            email="customer@example.com",
            password="SecureTestPassword123!",
        )

        self.open("/accounts/login/")

        self.browser.find_element(
            By.NAME,
            "username",
        ).send_keys(
            "testcustomer"
        )

        self.browser.find_element(
            By.NAME,
            "password",
        ).send_keys(
            "SecureTestPassword123!"
        )

        self.browser.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]',
        ).click()

        self.wait.until(
            EC.url_to_be(
                f"{self.live_server_url}/"
            )
        )

        self.assert_page_contains(
            "Logout"
        )


    def test_user_logout(self):
        User.objects.create_user(
            username="logoutuser",
            email="logout@example.com",
            password="SecureTestPassword123!",
        )

        self.open("/accounts/login/")

        self.browser.find_element(
            By.NAME,
            "username",
        ).send_keys(
            "logoutuser"
        )

        self.browser.find_element(
            By.NAME,
            "password",
        ).send_keys(
            "SecureTestPassword123!"
        )

        self.browser.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]',
        ).click()

        logout_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".nav-logout-button",
                )
            )
        )

        logout_button.click()

        self.wait.until(
            EC.url_to_be(
                f"{self.live_server_url}/"
            )
        )

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".nav-logout-button",
                )
            )
        )

        login_link = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'a[href="/accounts/login/"]',
                )
            )
        )

        self.assertTrue(
            login_link.is_displayed()
        )

        self.assertEqual(
            login_link.text.strip(),
            "Login",
        )