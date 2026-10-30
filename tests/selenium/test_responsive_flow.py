from decimal import Decimal

from catalog.models import Category, Product

from django.urls import reverse

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

        self.open(
            reverse("catalog:product-list")
        )

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

        self.open(
            reverse("catalog:product-list")
        )

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

    def create_marketplace_products(self):
        """
        Create enough active Products to verify the responsive
        Marketplace grid structure.
        """
        category = Category.objects.create(
            name="Responsive Gear",
            active=True,
        )

        for number in range(1, 4):
            Product.objects.create(
                category=category,
                name=(
                    f"Responsive Product {number}"
                ),
                description=(
                    "Responsive Marketplace test product."
                ),
                condition=Product.Condition.NEW,
                sgng_price=Decimal("24.99"),
                reference_price=Decimal("34.99"),
                inventory_quantity=3,
                active=True,
            )

    def test_marketplace_uses_three_columns_on_desktop(self):
        self.create_marketplace_products()

        self.browser.set_window_size(
            1440,
            1000,
        )

        self.open(
            reverse("catalog:product-list")
        )

        product_grid = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".product-grid",
                )
            )
        )

        columns = self.browser.execute_script(
            """
            return window.getComputedStyle(
                arguments[0]
            ).gridTemplateColumns;
            """,
            product_grid,
        )

        self.assertEqual(
            len(columns.split()),
            3,
        )

    def test_marketplace_uses_two_columns_on_tablet(self):
        self.create_marketplace_products()

        self.browser.set_window_size(
            820,
            1000,
        )

        self.open(
            reverse("catalog:product-list")
        )

        product_grid = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".product-grid",
                )
            )
        )

        columns = self.browser.execute_script(
            """
            return window.getComputedStyle(
                arguments[0]
            ).gridTemplateColumns;
            """,
            product_grid,
        )

        self.assertEqual(
            len(columns.split()),
            2,
        )

    def test_marketplace_uses_one_column_on_mobile(self):
        self.create_marketplace_products()

        self.browser.set_window_size(
            390,
            844,
        )

        self.open(
            reverse("catalog:product-list")
        )

        product_grid = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".product-grid",
                )
            )
        )

        columns = self.browser.execute_script(
            """
            return window.getComputedStyle(
                arguments[0]
            ).gridTemplateColumns;
            """,
            product_grid,
        )

        self.assertEqual(
            len(columns.split()),
            1,
        )

        filter_actions = (
            self.browser.find_element(
                By.CSS_SELECTOR,
                ".filter-actions",
            )
        )

        flex_direction = (
            self.browser.execute_script(
                """
                return window.getComputedStyle(
                    arguments[0]
                ).flexDirection;
                """,
                filter_actions,
            )
        )

        self.assertEqual(
            flex_direction,
            "column",
        )

    def tearDown(self):
        self.browser.maximize_window()