from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumTestCase(StaticLiveServerTestCase):
    """
    Shared Selenium foundation for the Cinematic SGnG Marketplace.

    StaticLiveServerTestCase starts a temporary Django test server
    and serves static files during browser-based tests.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = Options()

        # Keep the browser visible while developing/debugging.
        # Add "--headless=new" later if desired.
        options.add_argument("--start-maximized")

        cls.browser = webdriver.Edge(
            options=options
        )

        cls.browser.implicitly_wait(3)

        cls.wait = WebDriverWait(
            cls.browser,
            10,
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

        super().tearDownClass()

    def open(self, path="/"):
        """
        Open a path on Django's temporary Selenium test server.
        """

        self.browser.get(
            f"{self.live_server_url}{path}"
        )

    def assert_page_contains(self, text):
        """
        Convenience assertion for visible page text.
        """

        self.assertIn(
            text,
            self.browser.page_source,
        )

    def open_path(self, path):
        """
        Open a path relative to Django's Selenium live server.

        Examples:
            self.open_path("/")
            self.open_path("/contact/")
            self.open_path("/admin/login/")
        """

        if not path.startswith("/"):
            path = f"/{path}"

        url = f"{self.live_server_url}{path}"

        self.browser.get(url)

        self.wait.until(
            lambda driver:
            driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )


    def safe_click(self, locator, timeout=None):
        """
        Wait for an element, move it into the center of the
        viewport, and click it safely.

        locator must be a Selenium locator tuple, for example:

            (By.CSS_SELECTOR, 'button[type="submit"]')
        """

        wait = self.wait

        element = wait.until(
            EC.presence_of_element_located(
                locator
            )
        )

        self.browser.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: "instant",
                block: "center",
                inline: "center"
            });
            """,
            element,
        )

        wait.until(
            EC.visibility_of_element_located(
                locator
            )
        )

        element = wait.until(
            EC.element_to_be_clickable(
                locator
            )
        )

        try:
            element.click()

        except (
            ElementClickInterceptedException,
            StaleElementReferenceException,
        ):
            element = wait.until(
                EC.presence_of_element_located(
                    locator
                )
            )

            self.browser.execute_script(
                "arguments[0].click();",
                element,
            )


    def safe_click_element(self, element):
        """
        Safely click an element that has already been located.
        """

        self.browser.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: "instant",
                block: "center",
                inline: "center"
            });
            """,
            element,
        )

        try:
            element.click()

        except (
            ElementClickInterceptedException,
            StaleElementReferenceException,
        ):
            self.browser.execute_script(
                "arguments[0].click();",
                element,
            )


    def wait_for_url_contains(self, expected_path):
        """
        Wait until the browser URL contains the supplied path.
        """

        self.wait.until(
            EC.url_contains(
                expected_path
            )
        )
