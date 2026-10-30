from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SeleniumTestCase


class ContactFlowTests(SeleniumTestCase):
    """
    Browser-level Contact Form tests.
    """

    def test_contact_page_displays_form(self):
        self.open("/contact/")

        self.assert_page_contains(
            "Contact SGnG"
        )

        self.browser.find_element(
            By.NAME,
            "name",
        )

        self.browser.find_element(
            By.NAME,
            "email",
        )

        self.browser.find_element(
            By.NAME,
            "subject",
        )

        self.browser.find_element(
            By.NAME,
            "message",
        )


    def test_valid_contact_submission(self):
        """
        A visitor can submit valid Contact information and
        receive the success confirmation.
        """

        self.open_path(
            "/contact/"
        )

        self.browser.find_element(
            By.NAME,
            "name",
        ).send_keys(
            "Test User"
        )

        self.browser.find_element(
            By.NAME,
            "email",
        ).send_keys(
            "test@example.com"
        )

        self.browser.find_element(
            By.NAME,
            "subject",
        ).send_keys(
            "Marketplace inquiry"
        )

        self.browser.find_element(
            By.NAME,
            "message",
        ).send_keys(
            (
                "Please provide additional "
                "product information."
            )
        )

        self.safe_click(
            (
                By.CSS_SELECTOR,
                '.sgng-form button[type="submit"]',
            )
        )

        success_message = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".message.success",
                )
            )
        )

        self.assertIn(
            "received successfully",
            success_message.text.lower(),
        )


    def test_invalid_email_shows_error(self):
        """
        Submitting an invalid email address redisplays the
        Contact form with an email validation error.
        """

        self.open_path(
            "/contact/"
        )

        self.browser.find_element(
            By.NAME,
            "name",
        ).send_keys(
            "Test User"
        )

        self.browser.find_element(
            By.NAME,
            "email",
        ).send_keys(
            "invalid-email"
        )

        self.browser.find_element(
            By.NAME,
            "subject",
        ).send_keys(
            "Marketplace inquiry"
        )

        self.browser.find_element(
            By.NAME,
            "message",
        ).send_keys(
            (
                "Please provide additional "
                "product information."
            )
        )

        self.safe_click(
            (
                By.CSS_SELECTOR,
                '.sgng-form button[type="submit"]',
            )
        )

        email_error = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".form-errors",
                )
            )
        )

        self.assertIn(
            "valid email",
            email_error.text.lower(),
        )