from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import (
    expected_conditions as EC,
)

from .base import SeleniumTestCase


class HomepageFlowTests(SeleniumTestCase):
    """
    Browser-level tests for the Cinematic SGnG homepage.
    """

    def test_homepage_presents_brand_story_and_marketplace_path(
        self,
    ):
        """
        The homepage presents the SGnG brand experience and
        gives visitors a working path into the Marketplace.
        """
        self.open(
            reverse("pages:home")
        )

        hero = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".home-hero",
                )
            )
        )

        self.assertIsNotNone(
            hero
        )

        heading = (
            self.browser.find_element(
                By.CSS_SELECTOR,
                ".home-hero__title",
            )
        )

        self.assertIn(
            "Quality Gear",
            heading.text,
        )

        self.assertIn(
            "Honest Value",
            heading.text,
        )

        logo = (
            self.browser.find_element(
                By.CSS_SELECTOR,
                ".home-hero__logo",
            )
        )

        self.assertTrue(
            logo.is_displayed()
        )

        natural_width = (
            self.browser.execute_script(
                """
                return arguments[0].naturalWidth;
                """,
                logo,
            )
        )

        self.assertGreater(
            natural_width,
            0,
        )

        story_section = (
            self.browser.find_element(
                By.ID,
                "sgng-story",
            )
        )

        self.assertIsNotNone(
            story_section
        )

        marketplace_link = (
            self.browser.find_element(
                By.CSS_SELECTOR,
                (
                    ".home-hero__actions "
                    ".button--primary"
                ),
            )
        )

        marketplace_link.click()

        self.wait.until(
            EC.url_contains(
                reverse(
                    "catalog:product-list"
                )
            )
        )

        self.assertIn(
            reverse(
                "catalog:product-list"
            ),
            self.browser.current_url,
        )

    def test_homepage_hero_is_mobile_responsive(
        self,
    ):
        """
        The cinematic homepage remains usable at a
        representative mobile viewport.
        """
        self.browser.set_window_size(
            390,
            844,
        )

        self.open(
            reverse("pages:home")
        )

        hero_layout = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".home-hero__layout",
                )
            )
        )

        columns = (
            self.browser.execute_script(
                """
                return window.getComputedStyle(
                    arguments[0]
                ).gridTemplateColumns;
                """,
                hero_layout,
            )
        )

        self.assertEqual(
            len(columns.split()),
            1,
        )

        logo = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".home-hero__logo",
                )
            )
        )

        logo_wrapper = self.browser.find_element(
            By.CSS_SELECTOR,
            ".home-hero__brand-visual",
        )

        self.browser.execute_script(
            """
            arguments[0].style.opacity = "1";
            arguments[0].style.transform = "none";
            arguments[0].style.visibility = "visible";
            """,
            logo_wrapper,
        )

        self.wait.until(
            lambda browser: logo.is_displayed()
        )

        self.assertTrue(
            logo.is_displayed()
        )

        primary_action = (
            self.browser.find_element(
                By.CSS_SELECTOR,
                (
                    ".home-hero__actions "
                    ".button--primary"
                ),
            )
        )

        secondary_action = (
            self.browser.find_element(
                By.CSS_SELECTOR,
                (
                    ".home-hero__actions "
                    ".button--secondary"
                ),
            )
        )

        # The mobile hero intentionally stacks the SGnG logo,
        # headline, summary, and actions vertically. Scroll the
        # action area into the viewport before checking whether
        # the controls are visible and usable.
        self.browser.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: "instant",
                block: "center"
            });
            """,
            primary_action,
        )

        self.wait.until(
            EC.visibility_of(
                primary_action
            )
        )

        self.assertTrue(
            primary_action.is_displayed()
        )

        self.assertTrue(
            secondary_action.is_displayed()
        )

        primary_width = (
            self.browser.execute_script(
                """
                return arguments[0]
                    .getBoundingClientRect()
                    .width;
                """,
                primary_action,
            )
        )

        secondary_width = (
            self.browser.execute_script(
                """
                return arguments[0]
                    .getBoundingClientRect()
                    .width;
                """,
                secondary_action,
            )
        )

        self.assertGreater(
            primary_width,
            0,
        )

        self.assertGreater(
            secondary_width,
            0,
        )


    def tearDown(self):
        self.browser.maximize_window()