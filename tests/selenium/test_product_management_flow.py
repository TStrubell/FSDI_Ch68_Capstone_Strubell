from decimal import Decimal

from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from catalog.models import Category, Product
from .base import SeleniumTestCase


User = get_user_model()


class ProductManagementFlowTests(SeleniumTestCase):
    """
    End-to-end Selenium tests for SGnG Staff Product
    Management.

    These browser tests verify that a superuser can:

    1. Log into Django Admin.
    2. Open Product administration.
    3. Create a Product.
    4. Update a Product.
    5. Delete a Product.
    6. Verify the Product database changes caused by those
       browser interactions.

    Django application-level permission and CRUD tests remain
    in catalog/tests/test_staff_crud.py.
    """

    ADMIN_USERNAME = "seleniumadmin"
    ADMIN_EMAIL = "admin@example.com"
    ADMIN_PASSWORD = "SecureAdminPassword123!"

    PRODUCT_NAME = "Selenium Trail Product"
    UPDATED_PRODUCT_NAME = "Updated Selenium Trail Product"

    # =====================================================
    # TEST DATA
    # =====================================================

    def setUp(self):
        """
        Create isolated database records for each browser
        test.
        """

        super().setUp()

        self.admin_user = (
            User.objects.create_superuser(
                username=self.ADMIN_USERNAME,
                email=self.ADMIN_EMAIL,
                password=self.ADMIN_PASSWORD,
            )
        )

        self.category = Category.objects.create(
            name="Outdoor Gear",
            description="Outdoor test category.",
            active=True,
        )

    def wait_for_product_changelist(self):
        """
        Wait until Django Admin finishes the requested Product
        operation and redirects to the exact Product changelist.
        """
        product_changelist_url = (
            f"{self.live_server_url}"
            "/admin/catalog/product/"
        )

        self.wait.until(
            EC.url_to_be(
                product_changelist_url
            )
        )

        product_changelist = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "changelist",
                )
            )
        )

        return product_changelist

    # =====================================================
    # ADMIN LOGIN HELPER
    # =====================================================

    def admin_login(self):
        """
        Log the Selenium browser into Django Admin and wait
        until the administration index is displayed.
        """

        self.open_path("/admin/login/")

        username_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "username",
                )
            )
        )

        password_input = (
            self.browser.find_element(
                By.NAME,
                "password",
            )
        )

        username_input.clear()
        username_input.send_keys(
            self.ADMIN_USERNAME
        )

        password_input.clear()
        password_input.send_keys(
            self.ADMIN_PASSWORD
        )

        submit_button = (
            self.browser.find_element(
                By.CSS_SELECTOR,
                'input[type="submit"]',
            )
        )

        submit_button.click()

        self.wait.until(
            EC.url_contains(
                "/admin/"
            )
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "content-main",
                )
            )
        )

    # =====================================================
    # PRODUCT CREATION HELPER
    # =====================================================

    def create_product_through_admin(self):
        """
        Create the standard Selenium Product through the
        Django Admin browser interface.
        """
        self.browser.get(
            (
                f"{self.live_server_url}"
                "/admin/catalog/product/add/"
            )
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "name",
                )
            )
        )

        # Category
        category_select = Select(
            self.browser.find_element(
                By.NAME,
                "category",
            )
        )
        category_select.select_by_value(
            str(self.category.pk)
        )

        # Product Name
        name_input = (
            self.browser.find_element(
                By.NAME,
                "name",
            )
        )
        name_input.clear()
        name_input.send_keys(
            self.PRODUCT_NAME
        )

        # Description
        description_input = (
            self.browser.find_element(
                By.NAME,
                "description",
            )
        )
        description_input.clear()
        description_input.send_keys(
            (
                "Product created by Selenium "
                "for automated browser testing."
            )
        )

        # Condition
        condition_select = Select(
            self.browser.find_element(
                By.NAME,
                "condition",
            )
        )
        condition_select.select_by_value(
            Product.Condition.NEW
        )

        # SGnG Price
        price_input = (
            self.browser.find_element(
                By.NAME,
                "sgng_price",
            )
        )
        price_input.clear()
        price_input.send_keys(
            "39.99"
        )

        # Reference Price
        reference_price_input = (
            self.browser.find_element(
                By.NAME,
                "reference_price",
            )
        )
        reference_price_input.clear()
        reference_price_input.send_keys(
            "59.99"
        )

        # Inventory
        inventory_input = (
            self.browser.find_element(
                By.NAME,
                "inventory_quantity",
            )
        )
        inventory_input.clear()
        inventory_input.send_keys(
            "2"
        )

        # Active checkbox. Product.active normally defaults
        # to True, but ensure it remains enabled.
        active_checkbox = (
            self.browser.find_element(
                By.NAME,
                "active",
            )
        )

        if not active_checkbox.is_selected():
            active_checkbox.click()

        # Save Product
        save_button = (
            self.browser.find_element(
                By.NAME,
                "_save",
            )
        )
        save_button.click()

        # Wait for Django Admin to finish saving and redirect
        # to the exact Product changelist URL.
        self.wait_for_product_changelist()

        return Product.objects.get(
            name=self.PRODUCT_NAME
        )

    # =====================================================
    # PRODUCT ADMIN ACCESS
    # =====================================================

    def test_superuser_can_open_product_admin(self):
        """
        A superuser can log into Django Admin, open the
        Catalog Products section, and reach the Product
        changelist.
        """

        self.admin_login()

        # Confirm Admin index content.
        self.assertIn(
            "Site administration",
            self.browser.page_source,
        )

        self.assertIn(
            "Products",
            self.browser.page_source,
        )

        # Open Product administration.
        products_link = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    (
                        'a[href='
                        '"/admin/catalog/product/"]'
                    ),
                )
            )
        )

        products_link.click()

        # Confirm correct Product Admin URL.
        self.wait.until(
            EC.url_contains(
                "/admin/catalog/product/"
            )
        )

        self.assertIn(
            "/admin/catalog/product/",
            self.browser.current_url,
        )

        # Confirm the standard Django Admin Product
        # changelist rendered.
        product_changelist = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "changelist",
                )
            )
        )

        self.assertIsNotNone(
            product_changelist
        )

    # =====================================================
    # CREATE PRODUCT
    # =====================================================

    def test_superuser_can_create_product(self):
        """
        A superuser can create a marketplace Product through
        Django Admin.
        """

        self.admin_login()

        product = (
            self.create_product_through_admin()
        )

        self.assertTrue(
            Product.objects.filter(
                name=self.PRODUCT_NAME
            ).exists()
        )

        self.assertEqual(
            product.category,
            self.category,
        )

        self.assertEqual(
            product.condition,
            Product.Condition.NEW,
        )

        self.assertEqual(
            product.sgng_price,
            Decimal("39.99"),
        )

        self.assertEqual(
            product.reference_price,
            Decimal("59.99"),
        )

        self.assertEqual(
            product.inventory_quantity,
            2,
        )

        self.assertTrue(
            product.active
        )

        # Confirm the Product changelist rendered after
        # saving.
        product_changelist = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "changelist",
                )
            )
        )

        self.assertIsNotNone(
            product_changelist
        )

        self.assertIn(
            self.PRODUCT_NAME,
            self.browser.page_source,
        )

    # =====================================================
    # UPDATE PRODUCT
    # =====================================================

    def test_superuser_can_update_product(self):
        """
        A superuser can modify an existing Product through
        the Django Admin browser interface.
        """
        self.admin_login()

        product = (
            self.create_product_through_admin()
        )

        self.browser.get(
            (
                f"{self.live_server_url}"
                f"/admin/catalog/product/"
                f"{product.pk}/change/"
            )
        )

        name_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "name",
                )
            )
        )
        name_input.clear()
        name_input.send_keys(
            self.UPDATED_PRODUCT_NAME
        )

        price_input = (
            self.browser.find_element(
                By.NAME,
                "sgng_price",
            )
        )
        price_input.clear()
        price_input.send_keys(
            "34.99"
        )

        inventory_input = (
            self.browser.find_element(
                By.NAME,
                "inventory_quantity",
            )
        )
        inventory_input.clear()
        inventory_input.send_keys(
            "5"
        )

        save_button = (
            self.browser.find_element(
                By.NAME,
                "_save",
            )
        )
        save_button.click()

        # Do not use url_contains here. The Product change URL
        # already contains "/admin/catalog/product/" before the
        # form has finished saving.
        product_changelist = (
            self.wait_for_product_changelist()
        )

        # Refresh only after Django Admin has completed the save
        # and redirected to the Product changelist.
        product.refresh_from_db()

        self.assertEqual(
            product.name,
            self.UPDATED_PRODUCT_NAME,
        )
        self.assertEqual(
            product.sgng_price,
            Decimal("34.99"),
        )
        self.assertEqual(
            product.inventory_quantity,
            5,
        )

        self.assertIsNotNone(
            product_changelist
        )
        self.assertIn(
            self.UPDATED_PRODUCT_NAME,
            self.browser.page_source,
        )

    # =====================================================
    # DELETE PRODUCT
    # =====================================================

    def test_superuser_can_delete_product(self):
        """
        A superuser can delete an existing Product through
        the Django Admin confirmation workflow.
        """

        self.admin_login()

        product = (
            self.create_product_through_admin()
        )

        product_pk = product.pk

        self.browser.get(
            (
                f"{self.live_server_url}"
                f"/admin/catalog/product/"
                f"{product_pk}/delete/"
            )
        )

        # Django Admin delete confirmation page.
        confirmation_form = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'form[method="post"]',
                )
            )
        )

        self.assertIsNotNone(
            confirmation_form
        )

        self.assertIn(
            self.PRODUCT_NAME,
            self.browser.page_source,
        )

        # Django Admin's confirmation form includes a
        # submit input whose value is "Yes, I'm sure".
        delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    (
                        'input[type="submit"]'
                        '[value="Yes, I’m sure"], '
                        'input[type="submit"]'
                        '[value="Yes, I\'m sure"]'
                    ),
                )
            )
        )

        delete_button.click()

        product_changelist = (
            self.wait_for_product_changelist()
        )

        self.assertFalse(
            Product.objects.filter(
                pk=product_pk
            ).exists()
        )

        self.assertIsNotNone(
            product_changelist
        )

    # =====================================================
    # INVENTORY MANAGEMENT
    # =====================================================

    def test_superuser_can_update_inventory(self):
        """
        A superuser can change Product inventory through the
        Django Admin Product change form.
        """
        self.admin_login()

        product = (
            self.create_product_through_admin()
        )

        self.browser.get(
            (
                f"{self.live_server_url}"
                f"/admin/catalog/product/"
                f"{product.pk}/change/"
            )
        )

        inventory_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "inventory_quantity",
                )
            )
        )
        inventory_input.clear()
        inventory_input.send_keys(
            "0"
        )

        save_button = (
            self.browser.find_element(
                By.NAME,
                "_save",
            )
        )
        save_button.click()

        # Wait for the complete save-and-redirect cycle before
        # reading the Product from the test database.
        self.wait_for_product_changelist()

        product.refresh_from_db()

        self.assertEqual(
            product.inventory_quantity,
            0,
        )
        self.assertFalse(
            product.is_available
        )

    # =====================================================
    # CATEGORY MANAGEMENT ACCESS
    # =====================================================

    def test_superuser_can_open_category_admin(self):
        """
        A superuser can access Django Admin Category
        Management.
        """

        self.admin_login()

        self.browser.get(
            (
                f"{self.live_server_url}"
                "/admin/catalog/category/"
            )
        )

        self.wait.until(
            EC.url_contains(
                "/admin/catalog/category/"
            )
        )

        category_changelist = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "changelist",
                )
            )
        )

        self.assertIsNotNone(
            category_changelist
        )

        self.assertIn(
            self.category.name,
            self.browser.page_source,
        )