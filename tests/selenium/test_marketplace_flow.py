from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from catalog.models import Category, Product

from .base import SeleniumTestCase


class MarketplaceFlowTests(SeleniumTestCase):
    """
    Browser-level marketplace workflow tests.
    """

    def setUp(self):
        self.category = Category.objects.create(
            name="Outdoor Gear",
            description=(
                "Practical outdoor equipment "
                "for testing."
            ),
            active=True,
        )

        self.product = Product.objects.create(
            category=self.category,
            name="SGnG Trail Backpack",
            description=(
                "A versatile gently used "
                "trail backpack."
            ),
            condition=(
                Product.Condition.GENTLY_USED
            ),
            sgng_price=Decimal("49.99"),
            reference_price=Decimal("79.99"),
            inventory_quantity=1,
            featured=True,
            active=True,
        )


    def test_marketplace_displays_product(self):
        self.open("/marketplace/")

        self.assert_page_contains(
            "Marketplace"
        )

        self.assert_page_contains(
            "SGnG Trail Backpack"
        )

        self.assert_page_contains(
            "$49.99"
        )


    def test_product_detail_workflow(self):
        self.open("/marketplace/")

        product_link = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.LINK_TEXT,
                    "SGnG Trail Backpack",
                )
            )
        )

        product_link.click()

        self.wait.until(
            EC.url_contains(
                self.product.slug
            )
        )

        self.assert_page_contains(
            "SGnG Trail Backpack"
        )

        self.assert_page_contains(
            "$49.99"
        )

        self.assert_page_contains(
            "$79.99"
        )

        self.assert_page_contains(
            "In Stock"
        )


    def test_marketplace_search(self):
        self.open("/marketplace/")

        search = self.browser.find_element(
            By.NAME,
            "q",
        )

        search.send_keys(
            "Trail Backpack"
        )

        submit = self.browser.find_element(
            By.CSS_SELECTOR,
            ".marketplace-filters "
            'button[type="submit"]',
        )

        submit.click()

        self.assert_page_contains(
            "SGnG Trail Backpack"
        )


    def test_marketplace_empty_search_state(self):
        """
        A search with no matching Products displays the
        Marketplace empty-result state.
        """
        self.open(
            "/marketplace/"
        )

        search = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "q",
                )
            )
        )

        search.send_keys(
            "PRODUCT-DOES-NOT-EXIST"
        )

        submit = self.browser.find_element(
            By.CSS_SELECTOR,
            ".marketplace-filters "
            'button[type="submit"]',
        )

        submit.click()

        # Wait for the submitted search query to appear in
        # the resulting URL before inspecting the new page.
        self.wait.until(
            EC.url_contains(
                "q=PRODUCT-DOES-NOT-EXIST"
            )
        )

        # Wait for the actual empty-result state rendered by
        # the Marketplace template.
        empty_state = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".empty-state",
                )
            )
        )

        self.assertIsNotNone(
            empty_state
        )

        self.assertIn(
            "No Products Found",
            empty_state.text,
        )

        self.assertIn(
            (
                "No products match the current "
                "search or filter selections."
            ),
            empty_state.text,
        )

        view_all_link = (
            empty_state.find_element(
                By.LINK_TEXT,
                "View All Products",
            )
        )

        self.assertTrue(
            view_all_link.is_displayed()
        )


    def test_category_filter(self):
        self.open("/marketplace/")

        category_select = Select(
            self.browser.find_element(
                By.NAME,
                "category",
            )
        )

        category_select.select_by_value(
            self.category.slug
        )

        self.browser.find_element(
            By.CSS_SELECTOR,
            ".marketplace-filters "
            'button[type="submit"]',
        ).click()

        self.assert_page_contains(
            "SGnG Trail Backpack"
        )


    def test_condition_filter(self):
        self.open("/marketplace/")

        condition_select = Select(
            self.browser.find_element(
                By.NAME,
                "condition",
            )
        )

        condition_select.select_by_value(
            Product.Condition.GENTLY_USED
        )

        self.browser.find_element(
            By.CSS_SELECTOR,
            ".marketplace-filters "
            'button[type="submit"]',
        ).click()

        self.assert_page_contains(
            "Gently Used"
        )


    def test_sort_control_exists(self):
        self.open("/marketplace/")

        sort_control = Select(
            self.browser.find_element(
                By.NAME,
                "sort",
            )
        )

        values = [
            option.get_attribute("value")
            for option
            in sort_control.options
        ]

        self.assertIn(
            "price_low",
            values,
        )

        self.assertIn(
            "price_high",
            values,
        )


    def test_clear_filters(self):
        self.open(
            "/marketplace/?q=Trail"
        )

        clear_link = self.browser.find_element(
            By.LINK_TEXT,
            "Clear",
        )

        clear_link.click()

        self.wait.until(
            EC.url_matches(
                rf"{self.live_server_url}"
                r"/marketplace/?$"
            )
        )

        search = self.browser.find_element(
            By.NAME,
            "q",
        )

        self.assertEqual(
            search.get_attribute("value"),
            "",
        )