from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from catalog.models import Category, Product
from .base import SeleniumTestCase


class MarketplaceFlowTests(SeleniumTestCase):
    """
    Browser-level Marketplace workflow tests.
    """

    SEARCH_INPUT_LOCATOR = (
        By.NAME,
        "q",
    )

    CATEGORY_SELECT_LOCATOR = (
        By.NAME,
        "category",
    )

    CONDITION_SELECT_LOCATOR = (
        By.NAME,
        "condition",
    )

    SORT_SELECT_LOCATOR = (
        By.NAME,
        "sort",
    )

    FILTER_SUBMIT_LOCATOR = (
        By.CSS_SELECTOR,
        '.marketplace-filters button[type="submit"]',
    )

    CLEAR_FILTERS_LOCATOR = (
        By.LINK_TEXT,
        "Clear",
    )

    EMPTY_STATE_LOCATOR = (
        By.CSS_SELECTOR,
        ".empty-state",
    )

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

    def create_product(
        self,
        *,
        name,
        description,
        sgng_price,
        reference_price,
        inventory_quantity,
        active=True,
        featured=False,
        condition=None,
    ):
        """
        Create an additional Product for a focused browser
        workflow test.
        """
        return Product.objects.create(
            category=self.category,
            name=name,
            description=description,
            condition=(
                condition
                or Product.Condition.NEW
            ),
            sgng_price=Decimal(
                str(sgng_price)
            ),
            reference_price=Decimal(
                str(reference_price)
            ),
            inventory_quantity=inventory_quantity,
            active=active,
            featured=featured,
        )

    def submit_marketplace_filters(self):
        """
        Submit the Marketplace filter form using the shared
        locator-based safe-click helper.
        """
        self.safe_click(
            self.FILTER_SUBMIT_LOCATOR
        )

        self.wait_for_document_ready()

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
        """
        Verify that a visitor can open the Marketplace,
        select a Product, and reach the corresponding
        Product Detail page.
        """
        product = self.create_product(
            name="Selenium Trail Product",
            description=(
                "Product created for the Selenium "
                "Marketplace detail workflow."
            ),
            sgng_price="39.99",
            reference_price="59.99",
            inventory_quantity=3,
            active=True,
            featured=True,
        )

        self.open_path(
            "/marketplace/"
        )

        self.wait_for_document_ready()

        product_card_locator = (
            By.XPATH,
            (
                "//article[contains("
                "concat(' ', normalize-space(@class), ' '), "
                "' product-card '"
                ")]"
                f"[contains(normalize-space(.), '{product.name}')]"
            ),
        )

        self.wait.until(
            EC.visibility_of_element_located(
                product_card_locator
            )
        )

        product_link_locator = (
            By.XPATH,
            (
                "//article[contains("
                "concat(' ', normalize-space(@class), ' '), "
                "' product-card '"
                ")]"
                f"[contains(normalize-space(.), '{product.name}')]"
                "//a[normalize-space()='View Details']"
            ),
        )

        self.safe_click(
            product_link_locator
        )

        expected_url = (
            f"{self.live_server_url}"
            f"{product.get_absolute_url()}"
        )

        self.wait.until(
            EC.url_to_be(
                expected_url
            )
        )

        self.wait_for_document_ready()

        detail_heading_locator = (
            By.CSS_SELECTOR,
            ".product-detail__content h1",
        )

        detail_heading = self.wait.until(
            EC.visibility_of_element_located(
                detail_heading_locator
            )
        )

        self.assertTrue(
            detail_heading.is_displayed()
        )

        self.assertEqual(
            detail_heading.text.strip(),
            product.name,
        )

        self.assertEqual(
            self.browser.current_url,
            expected_url,
        )

        self.assert_page_contains(
            product.description
        )

        self.assert_page_contains(
            "39.99"
        )

        self.assert_page_contains(
            "In Stock: 3"
        )

    def test_marketplace_search(self):
        self.open("/marketplace/")

        search = self.wait.until(
            EC.visibility_of_element_located(
                self.SEARCH_INPUT_LOCATOR
            )
        )

        search.send_keys(
            "Trail Backpack"
        )

        self.submit_marketplace_filters()

        self.wait.until(
            EC.url_contains(
                "q=Trail+Backpack"
            )
        )

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
                self.SEARCH_INPUT_LOCATOR
            )
        )

        search.send_keys(
            "PRODUCT-DOES-NOT-EXIST"
        )

        self.submit_marketplace_filters()

        self.wait.until(
            EC.url_contains(
                "q=PRODUCT-DOES-NOT-EXIST"
            )
        )

        empty_state = self.wait.until(
            EC.visibility_of_element_located(
                self.EMPTY_STATE_LOCATOR
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

        view_all_link = empty_state.find_element(
            By.LINK_TEXT,
            "View All Products",
        )

        self.assertTrue(
            view_all_link.is_displayed()
        )

    def test_category_filter(self):
        self.open("/marketplace/")

        category_element = self.wait.until(
            EC.element_to_be_clickable(
                self.CATEGORY_SELECT_LOCATOR
            )
        )

        category_select = Select(
            category_element
        )

        category_select.select_by_value(
            self.category.slug
        )

        self.submit_marketplace_filters()

        self.wait.until(
            EC.url_contains(
                f"category={self.category.slug}"
            )
        )

        self.assert_page_contains(
            "SGnG Trail Backpack"
        )

    def test_condition_filter(self):
        self.open("/marketplace/")

        condition_element = self.wait.until(
            EC.element_to_be_clickable(
                self.CONDITION_SELECT_LOCATOR
            )
        )

        condition_select = Select(
            condition_element
        )

        condition_select.select_by_value(
            Product.Condition.GENTLY_USED
        )

        self.submit_marketplace_filters()

        self.wait.until(
            EC.url_contains(
                (
                    "condition="
                    f"{Product.Condition.GENTLY_USED}"
                )
            )
        )

        self.assert_page_contains(
            "Gently Used"
        )

    def test_sort_control_exists(self):
        self.open("/marketplace/")

        sort_element = self.wait.until(
            EC.presence_of_element_located(
                self.SORT_SELECT_LOCATOR
            )
        )

        sort_control = Select(
            sort_element
        )

        values = [
            option.get_attribute("value")
            for option in sort_control.options
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

        self.safe_click(
            self.CLEAR_FILTERS_LOCATOR
        )

        expected_url = (
            f"{self.live_server_url}"
            "/marketplace/"
        )

        self.wait.until(
            EC.url_to_be(
                expected_url
            )
        )

        self.wait_for_document_ready()

        search = self.wait.until(
            EC.visibility_of_element_located(
                self.SEARCH_INPUT_LOCATOR
            )
        )

        self.assertEqual(
            search.get_attribute("value"),
            "",
        )
