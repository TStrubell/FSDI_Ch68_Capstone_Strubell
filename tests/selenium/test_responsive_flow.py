from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SeleniumTestCase


class ResponsiveFlowTests(SeleniumTestCase):
    """
    Browser-level responsive interface tests.
    """

    def test_mobile_navigation_opens(self):
        self.browser.set_window_size(
            390,
            844,
        )

        self.open("/")

        toggle = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".nav-toggle",
                )
            )
        )

        toggle.click()

        navigation = (
            self.browser.find_element(
                By.ID,
                "primary-navigation",
            )
        )

        self.assertIn(
            "is-open",
            navigation.get_attribute(
                "class"
            ),
        )


    def test_mobile_navigation_closes_with_escape(self):
        self.browser.set_window_size(
            390,
            844,
        )

        self.open("/")

        toggle = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".nav-toggle",
                )
            )
        )

        toggle.click()

        self.browser.find_element(
            By.TAG_NAME,
            "body",
        ).send_keys(
            "\ue00c"
        )

        navigation = (
            self.browser.find_element(
                By.ID,
                "primary-navigation",
            )
        )

        self.wait.until(
            lambda driver:
                "is-open"
                not in navigation.get_attribute(
                    "class"
                )
        )

        self.assertNotIn(
            "is-open",
            navigation.get_attribute(
                "class"
            ),
        )


    def tearDown(self):
        self.browser.maximize_window()