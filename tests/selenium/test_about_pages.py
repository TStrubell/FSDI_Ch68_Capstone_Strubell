from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SeleniumTestCase


class AboutPagesTests(SeleniumTestCase):
    """
    End-to-end Selenium tests for the Cinematic SGnG
    About experience.

    These tests verify:

    1. The main About page loads.
    2. The primary About heading is displayed.
    3. The About avatar is displayed and properly constrained.
    4. All four About story cards are present.
    5. Each story card opens its dedicated detail page.
    6. Each detail page can return to the main About page.
    7. The Marketplace and Home actions navigate correctly.
    """

    ABOUT_MAIN_LOCATOR = (
        By.CSS_SELECTOR,
        ".story-section",
    )

    ABOUT_HEADING_LOCATOR = (
        By.CSS_SELECTOR,
        ".about-intro__content h1",
    )

    ABOUT_AVATAR_LOCATOR = (
        By.CSS_SELECTOR,
        "img.about-intro__avatar",
    )

    ABOUT_CARD_LOCATOR = (
        By.CSS_SELECTOR,
        "a.story-card--link",
    )

    DETAIL_PAGE_LOCATOR = (
        By.CSS_SELECTOR,
        ".about-detail",
    )

    DETAIL_HEADING_LOCATOR = (
        By.CSS_SELECTOR,
        ".about-detail-title",
    )

    RETURN_TO_ABOUT_LOCATOR = (
        By.CSS_SELECTOR,
        "a.about-detail-link",
    )

    MARKETPLACE_LINK_LOCATOR = (
        By.XPATH,
        (
            "//a[contains(@class, 'button--primary') "
            "and normalize-space()='Explore Marketplace']"
        ),
    )

    RETURN_HOME_LINK_LOCATOR = (
        By.XPATH,
        (
            "//a[contains(@class, 'button--secondary') "
            "and normalize-space()='Return Home']"
        ),
    )

    def build_url(self, url_name):
        """
        Build a complete live-server URL from a named
        Django URL pattern.
        """
        return (
            f"{self.live_server_url}"
            f"{reverse(url_name)}"
        )

    def open_named_page(self, url_name):
        """
        Open a named Django route through the temporary
        Selenium live server and wait for the document
        to finish loading.
        """
        expected_url = self.build_url(
            url_name
        )

        self.browser.get(
            expected_url
        )

        self.wait_for_document_ready()

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.TAG_NAME,
                    "body",
                )
            )
        )

        self.assertEqual(
            self.browser.current_url,
            expected_url,
        )

        return expected_url

    def open_about_page(self):
        """
        Open the main SGnG About page and wait for the
        principal About section to become visible.
        """
        expected_url = self.open_named_page(
            "pages:about"
        )

        about_section = self.wait.until(
            EC.visibility_of_element_located(
                self.ABOUT_MAIN_LOCATOR
            )
        )

        self.assertTrue(
            about_section.is_displayed()
        )

        return expected_url

    def open_detail_page_from_card(
        self,
        card_text,
        expected_route,
        expected_heading,
    ):
        """
        Open the main About page, select the requested
        story card, and verify the resulting detail page.
        """
        self.open_about_page()

        card_locator = (
            By.XPATH,
            (
                "//a[contains("
                "concat(' ', normalize-space(@class), ' '), "
                "' story-card--link '"
                ")]"
                f"[contains(normalize-space(.), '{card_text}')]"
            ),
        )

        self.safe_click(
            card_locator
        )

        expected_url = self.build_url(
            expected_route
        )

        self.wait.until(
            EC.url_to_be(
                expected_url
            )
        )

        self.wait_for_document_ready()

        detail_page = self.wait.until(
            EC.visibility_of_element_located(
                self.DETAIL_PAGE_LOCATOR
            )
        )

        self.assertTrue(
            detail_page.is_displayed()
        )

        heading = self.wait.until(
            EC.visibility_of_element_located(
                self.DETAIL_HEADING_LOCATOR
            )
        )

        self.assertEqual(
            heading.text.strip(),
            expected_heading,
        )

        self.assertEqual(
            self.browser.current_url,
            expected_url,
        )

    def verify_return_to_about(self):
        """
        Select the detail page's return link and verify
        navigation back to the SGnG About page.
        """
        self.safe_click(
            self.RETURN_TO_ABOUT_LOCATOR
        )

        expected_about_url = self.build_url(
            "pages:about"
        )

        self.wait.until(
            EC.url_to_be(
                expected_about_url
            )
        )

        self.wait_for_document_ready()

        about_section = self.wait.until(
            EC.visibility_of_element_located(
                self.ABOUT_MAIN_LOCATOR
            )
        )

        self.assertTrue(
            about_section.is_displayed()
        )

    # =====================================================
    # MAIN ABOUT PAGE
    # =====================================================

    def test_about_page_loads(self):
        """
        Verify that the main SGnG About page loads and
        displays its principal content section.
        """
        expected_url = self.open_about_page()

        self.assertEqual(
            self.browser.current_url,
            expected_url,
        )

        self.assert_page_contains(
            "The SGnG Story"
        )

    def test_about_page_heading(self):
        """
        Verify the primary heading displayed on the
        SGnG About page.
        """
        self.open_about_page()

        heading = self.wait.until(
            EC.visibility_of_element_located(
                self.ABOUT_HEADING_LOCATOR
            )
        )

        self.assertTrue(
            heading.is_displayed()
        )

        self.assertEqual(
            heading.text.strip(),
            "The SGnG Story",
        )

    def test_about_avatar_is_present_and_constrained(self):
        """
        Verify that the About avatar is visible, has
        meaningful image attributes, and is rendered with
        the compact dimensions defined by about.css.
        """
        self.open_about_page()

        avatar = self.wait.until(
            EC.visibility_of_element_located(
                self.ABOUT_AVATAR_LOCATOR
            )
        )

        self.assertTrue(
            avatar.is_displayed()
        )

        self.assertTrue(
            avatar.get_attribute("src")
        )

        self.assertTrue(
            avatar.get_attribute("alt")
        )

        rendered_width = avatar.size["width"]
        rendered_height = avatar.size["height"]

        self.assertGreater(
            rendered_width,
            0,
        )

        self.assertGreater(
            rendered_height,
            0,
        )

        # Desktop about.css limits the portrait to a compact
        # presentation rather than the earlier tall capsule.
        self.assertLessEqual(
            rendered_width,
            320,
        )

        self.assertLessEqual(
            rendered_height,
            390,
        )

        object_fit = self.browser.execute_script(
            """
            return window.getComputedStyle(
                arguments[0]
            ).objectFit;
            """,
            avatar,
        )

        self.assertEqual(
            object_fit,
            "cover",
        )

    def test_four_about_story_cards_are_present(self):
        """
        Verify that all four clickable About story cards
        are present and have valid destination links.
        """
        self.open_about_page()

        cards = self.wait.until(
            EC.visibility_of_all_elements_located(
                self.ABOUT_CARD_LOCATOR
            )
        )

        self.assertEqual(
            len(cards),
            4,
        )

        card_text = [
            card.text
            for card in cards
        ]

        self.assertTrue(
            any(
                "Military Service" in text
                for text in card_text
            )
        )

        self.assertTrue(
            any(
                "Craftsmanship" in text
                for text in card_text
            )
        )

        self.assertTrue(
            any(
                "Entrepreneurship" in text
                for text in card_text
            )
        )

        self.assertTrue(
            any(
                "Software Development" in text
                for text in card_text
            )
        )

        for card in cards:
            self.assertTrue(
                card.get_attribute("href")
            )

    # =====================================================
    # ABOUT DETAIL-PAGE NAVIGATION
    # =====================================================

    def test_military_service_card_navigation(self):
        """
        Verify that the Military Service card opens the
        dedicated Military Service page.
        """
        self.open_detail_page_from_card(
            card_text="Military Service",
            expected_route="pages:military_service",
            expected_heading="🎖️ Military Service",
        )

        self.verify_return_to_about()

    def test_craftsmanship_card_navigation(self):
        """
        Verify that the Craftsmanship card opens the
        dedicated Craftsmanship page.
        """
        self.open_detail_page_from_card(
            card_text="Craftsmanship",
            expected_route="pages:craftsmanship",
            expected_heading="🧰 Craftsmanship",
        )

        self.verify_return_to_about()

    def test_entrepreneurship_card_navigation(self):
        """
        Verify that the Entrepreneurship card opens the
        dedicated Entrepreneurship page.
        """
        self.open_detail_page_from_card(
            card_text="Entrepreneurship",
            expected_route="pages:entrepreneurship",
            expected_heading="💼 Entrepreneurship",
        )

        self.verify_return_to_about()

    def test_software_development_card_navigation(self):
        """
        Verify that the Software Development card opens the
        dedicated Software Development page.
        """
        self.open_detail_page_from_card(
            card_text="Software Development",
            expected_route="pages:software_development",
            expected_heading="💻 Software Development",
        )

        self.verify_return_to_about()

    # =====================================================
    # MAIN ABOUT-PAGE ACTIONS
    # =====================================================

    def test_explore_marketplace_navigation(self):
        """
        Verify that Explore Marketplace opens the Catalog
        Product List page.
        """
        self.open_about_page()

        self.safe_click(
            self.MARKETPLACE_LINK_LOCATOR
        )

        expected_url = self.build_url(
            "catalog:product-list"
        )

        self.wait.until(
            EC.url_to_be(
                expected_url
            )
        )

        self.wait_for_document_ready()

        self.assertEqual(
            self.browser.current_url,
            expected_url,
        )

    def test_return_home_navigation(self):
        """
        Verify that Return Home opens the SGnG Home page.
        """
        self.open_about_page()

        self.safe_click(
            self.RETURN_HOME_LINK_LOCATOR
        )

        expected_url = self.build_url(
            "pages:home"
        )

        self.wait.until(
            EC.url_to_be(
                expected_url
            )
        )

        self.wait_for_document_ready()

        self.assertEqual(
            self.browser.current_url,
            expected_url,
        )