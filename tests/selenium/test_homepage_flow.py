from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SeleniumTestCase


class HomepageFlowTests(SeleniumTestCase):
    """
    Browser-level tests for the Cinematic SGnG homepage.
    """

    HERO_LOCATOR = (
        By.CSS_SELECTOR,
        ".home-hero",
    )

    HERO_TITLE_LOCATOR = (
        By.CSS_SELECTOR,
        ".home-hero__title",
    )

    HERO_LOGO_LOCATOR = (
        By.CSS_SELECTOR,
        ".home-hero__logo",
    )

    STORY_SECTION_LOCATOR = (
        By.ID,
        "sgng-story",
    )

    MARKETPLACE_LINK_LOCATOR = (
        By.CSS_SELECTOR,
        ".home-hero__actions .button--primary",
    )

    HERO_LAYOUT_LOCATOR = (
        By.CSS_SELECTOR,
        ".home-hero__layout",
    )

    HERO_BRAND_VISUAL_LOCATOR = (
        By.CSS_SELECTOR,
        ".home-hero__brand-visual",
    )

    SECONDARY_ACTION_LOCATOR = (
        By.CSS_SELECTOR,
        ".home-hero__actions .button--secondary",
    )

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
                self.HERO_LOCATOR
            )
        )

        self.assertIsNotNone(
            hero
        )

        heading = self.wait.until(
            EC.visibility_of_element_located(
                self.HERO_TITLE_LOCATOR
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

        logo = self.wait.until(
            EC.visibility_of_element_located(
                self.HERO_LOGO_LOCATOR
            )
        )

        self.assertTrue(
            logo.is_displayed()
        )

        natural_width = self.browser.execute_script(
            """
            return arguments[0].naturalWidth;
            """,
            logo,
        )

        self.assertGreater(
            natural_width,
            0,
        )

        story_section = self.wait.until(
            EC.presence_of_element_located(
                self.STORY_SECTION_LOCATOR
            )
        )

        self.assertIsNotNone(
            story_section
        )

        self.safe_click(
            self.MARKETPLACE_LINK_LOCATOR
        )

        expected_path = reverse(
            "catalog:product-list"
        )

        self.wait.until(
            EC.url_contains(
                expected_path
            )
        )

        self.wait_for_document_ready()

        self.assertIn(
            expected_path,
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
                self.HERO_LAYOUT_LOCATOR
            )
        )

        columns = self.browser.execute_script(
            """
            return window.getComputedStyle(
                arguments[0]
            ).gridTemplateColumns;
            """,
            hero_layout,
        )

        self.assertEqual(
            len(columns.split()),
            1,
        )

        logo = self.wait.until(
            EC.presence_of_element_located(
                self.HERO_LOGO_LOCATOR
            )
        )

        logo_wrapper = self.wait.until(
            EC.presence_of_element_located(
                self.HERO_BRAND_VISUAL_LOCATOR
            )
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

        primary_action = self.wait.until(
            EC.presence_of_element_located(
                self.MARKETPLACE_LINK_LOCATOR
            )
        )

        secondary_action = self.wait.until(
            EC.presence_of_element_located(
                self.SECONDARY_ACTION_LOCATOR
            )
        )

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
            EC.visibility_of_element_located(
                self.MARKETPLACE_LINK_LOCATOR
            )
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.SECONDARY_ACTION_LOCATOR
            )
        )

        self.assertTrue(
            primary_action.is_displayed()
        )

        self.assertTrue(
            secondary_action.is_displayed()
        )

        primary_width = self.browser.execute_script(
            """
            return arguments[0]
                .getBoundingClientRect()
                .width;
            """,
            primary_action,
        )

        secondary_width = self.browser.execute_script(
            """
            return arguments[0]
                .getBoundingClientRect()
                .width;
            """,
            secondary_action,
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
