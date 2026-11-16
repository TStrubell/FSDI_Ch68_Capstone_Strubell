from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
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

        # Keep Microsoft Edge visible during development and debugging.
        # Add "--headless=new" later if headless execution is desired.
        options.add_argument("--start-maximized")

        # Reduce browser behaviors that can interfere with test controls.
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        cls.browser = webdriver.Edge(options=options)

        # Keep implicit waiting short because explicit waits are used
        # throughout the Selenium test suite.
        cls.browser.implicitly_wait(2)

        cls.wait = WebDriverWait(
            cls.browser,
            15,
            ignored_exceptions=(
                StaleElementReferenceException,
            ),
        )

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "browser"):
            cls.browser.quit()

        super().tearDownClass()

    def open(self, path="/"):
        """
        Open a path on Django's temporary Selenium test server and
        wait until the document reports that loading is complete.
        """
        self.open_path(path)

    def open_path(self, path="/"):
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
            lambda driver: driver.execute_script(
                "return document.readyState"
            )
            == "complete"
        )

    def assert_page_contains(self, text):
        """
        Assert that the supplied text appears in the current page source.
        """
        self.assertIn(
            text,
            self.browser.page_source,
        )

    def safe_click(self, locator, timeout=None):
        """
        Wait for an element, center it in the viewport, verify that
        the center click point is unobstructed, and perform a normal
        Selenium pointer click.

        locator must be a Selenium locator tuple, for example:

            (By.CSS_SELECTOR, 'button[type="submit"]')
        """
        wait_time = timeout if timeout is not None else 15

        wait = WebDriverWait(
            self.browser,
            wait_time,
            ignored_exceptions=(
                StaleElementReferenceException,
            ),
        )

        element = wait.until(
            EC.presence_of_element_located(locator)
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
            EC.visibility_of_element_located(locator)
        )

        def click_point_is_clear(driver):
            try:
                current_element = driver.find_element(*locator)

                return driver.execute_script(
                    """
                    const target = arguments[0];
                    const rectangle = target.getBoundingClientRect();

                    const x =
                        rectangle.left + (rectangle.width / 2);

                    const y =
                        rectangle.top + (rectangle.height / 2);

                    const topElement =
                        document.elementFromPoint(x, y);

                    return (
                        topElement === target ||
                        target.contains(topElement)
                    );
                    """,
                    current_element,
                )
            except StaleElementReferenceException:
                return False

        try:
            wait.until(click_point_is_clear)
        except TimeoutException:
            # Re-center the target before the final click attempt.
            element = wait.until(
                EC.presence_of_element_located(locator)
            )

            self.browser.execute_script(
                """
                arguments[0].scrollIntoView({
                    behavior: "instant",
                    block: "center",
                    inline: "center"
                });

                window.scrollBy(0, -20);
                """,
                element,
            )

        element = wait.until(
            EC.element_to_be_clickable(locator)
        )

        try:
            ActionChains(self.browser).move_to_element(
                element
            ).pause(0.2).click().perform()

        except (
            ElementClickInterceptedException,
            StaleElementReferenceException,
        ):
            element = wait.until(
                EC.presence_of_element_located(locator)
            )

            self.browser.execute_script(
                """
                arguments[0].scrollIntoView({
                    behavior: "instant",
                    block: "center",
                    inline: "center"
                });

                window.scrollBy(0, -20);
                """,
                element,
            )

            element = wait.until(
                EC.element_to_be_clickable(locator)
            )

            ActionChains(self.browser).move_to_element(
                element
            ).pause(0.3).click().perform()

    def safe_click_element(self, element, timeout=None):
        """
        Safely click an element that has already been located.

        Use safe_click(locator) whenever possible because a locator
        allows Selenium to relocate an element if the DOM changes.
        """
        wait_time = timeout if timeout is not None else 15

        wait = WebDriverWait(
            self.browser,
            wait_time,
            ignored_exceptions=(
                StaleElementReferenceException,
            ),
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
            lambda driver: (
                element.is_displayed()
                and element.is_enabled()
            )
        )

        try:
            ActionChains(self.browser).move_to_element(
                element
            ).pause(0.2).click().perform()

        except ElementClickInterceptedException:
            self.browser.execute_script(
                """
                arguments[0].scrollIntoView({
                    behavior: "instant",
                    block: "center",
                    inline: "center"
                });

                window.scrollBy(0, -20);
                """,
                element,
            )

            ActionChains(self.browser).move_to_element(
                element
            ).pause(0.3).click().perform()

    def wait_for_url_contains(self, expected_path, timeout=None):
        """
        Wait until the browser URL contains the supplied path.
        """
        wait_time = timeout if timeout is not None else 15

        WebDriverWait(
            self.browser,
            wait_time,
        ).until(
            EC.url_contains(expected_path)
        )

    def wait_for_document_ready(self, timeout=None):
        """
        Wait until the browser reports that the current document
        has finished loading.
        """
        wait_time = timeout if timeout is not None else 15

        WebDriverWait(
            self.browser,
            wait_time,
        ).until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            )
            == "complete"
        )
        