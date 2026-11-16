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
    End-to-end Selenium tests for SGnG staff product management.

    These browser tests verify that a superuser can:

    1. Log in to Django Admin.
    2. Open Product administration.
    3. Create a Product.
    4. Update a Product.
    5. Delete a Product.
    6. Update Product inventory.
    7. Open Category administration.

    Django application-level permission and CRUD tests remain
    in catalog/tests/test_staff_crud.py.
    """

    ADMIN_USERNAME = "seleniumadmin"
    ADMIN_EMAIL = "admin@example.com"
    ADMIN_PASSWORD = "SecureAdminPassword123!"

    PRODUCT_NAME = "Selenium Trail Product"
    UPDATED_PRODUCT_NAME = "Updated Selenium Trail Product"

    ADMIN_LOGIN_PATH = "/admin/login/"
    ADMIN_INDEX_PATH = "/admin/"
    PRODUCT_ADMIN_PATH = "/admin/catalog/product/"
    PRODUCT_ADD_PATH = "/admin/catalog/product/add/"
    CATEGORY_ADMIN_PATH = "/admin/catalog/category/"

    USERNAME_LOCATOR = (
        By.NAME,
        "username",
    )

    PASSWORD_LOCATOR = (
        By.NAME,
        "password",
    )

    ADMIN_LOGIN_SUBMIT_LOCATOR = (
        By.CSS_SELECTOR,
        'input[type="submit"]',
    )

    ADMIN_CONTENT_LOCATOR = (
        By.ID,
        "content-main",
    )

    PRODUCT_CHANGELIST_LOCATOR = (
        By.ID,
        "changelist",
    )

    PRODUCT_FORM_LOCATOR = (
        By.CSS_SELECTOR,
        'input[name="name"]',
    )

    CATEGORY_CHANGELIST_LOCATOR = (
        By.ID,
        "changelist",
    )

    PRODUCTS_LINK_LOCATOR = (
        By.CSS_SELECTOR,
        'a[href="/admin/catalog/product/"]',
    )

    CATEGORY_FIELD_LOCATOR = (
        By.NAME,
        "category",
    )

    NAME_FIELD_LOCATOR = (
        By.NAME,
        "name",
    )

    DESCRIPTION_FIELD_LOCATOR = (
        By.NAME,
        "description",
    )

    CONDITION_FIELD_LOCATOR = (
        By.NAME,
        "condition",
    )

    SGNG_PRICE_FIELD_LOCATOR = (
        By.NAME,
        "sgng_price",
    )

    REFERENCE_PRICE_FIELD_LOCATOR = (
        By.NAME,
        "reference_price",
    )

    INVENTORY_FIELD_LOCATOR = (
        By.NAME,
        "inventory_quantity",
    )

    ACTIVE_FIELD_LOCATOR = (
        By.NAME,
        "active",
    )

    SAVE_BUTTON_LOCATOR = (
        By.NAME,
        "_save",
    )

    DELETE_CONFIRMATION_FORM_LOCATOR = (
        By.CSS_SELECTOR,
        'form[method="post"]',
    )

    DELETE_CONFIRMATION_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        'form[method="post"] input[type="submit"]',
    )

    # =====================================================
    # TEST DATA
    # =====================================================

    def setUp(self):
        """
        Create isolated database records for each browser test.
        """
        super().setUp()

        self.admin_user = User.objects.create_superuser(
            username=self.ADMIN_USERNAME,
            email=self.ADMIN_EMAIL,
            password=self.ADMIN_PASSWORD,
        )

        self.category = Category.objects.create(
            name="Outdoor Gear",
            description="Outdoor test category.",
            active=True,
        )

    # =====================================================
    # GENERAL HELPERS
    # =====================================================

    def admin_url(self, path):
        """
        Build a complete URL for a Django Admin path.
        """
        if not path.startswith("/"):
            path = f"/{path}"

        return f"{self.live_server_url}{path}"

    def wait_for_admin_content(self):
        """
        Wait for a general Django Admin page that is known to
        render the primary #content-main container.

        Specialized Product forms, changelists, Category lists,
        and delete-confirmation pages use their own wait helpers.
        """
        self.wait_for_document_ready()

        content_main = self.wait.until(
            EC.presence_of_element_located(
                self.ADMIN_CONTENT_LOCATOR
            )
        )

        self.assertIsNotNone(
            content_main
        )

        return content_main

    def wait_for_product_changelist(self):
        """
        Wait until Django Admin finishes the requested Product
        operation and visibly renders the exact Product changelist.
        """
        expected_url = self.admin_url(
            self.PRODUCT_ADMIN_PATH
        )

        self.wait.until(
            EC.url_to_be(
                expected_url
            )
        )

        self.wait_for_document_ready()

        product_changelist = self.wait.until(
            EC.visibility_of_element_located(
                self.PRODUCT_CHANGELIST_LOCATOR
            )
        )

        self.assertIsNotNone(
            product_changelist
        )

        return product_changelist

    def wait_for_product_form(self):
        """
        Wait until a Django Admin Product add or change form
        is fully available for interaction.
        """
        self.wait_for_document_ready()

        name_input = self.wait.until(
            EC.element_to_be_clickable(
                self.PRODUCT_FORM_LOCATOR
            )
        )

        self.assertIsNotNone(
            name_input
        )

        return name_input

    def wait_for_delete_confirmation(
        self,
        expected_delete_url=None,
    ):
        """
        Wait until the Django Admin Product delete-confirmation
        page has fully rendered.
        """
        self.wait_for_document_ready()

        if expected_delete_url is not None:
            self.wait.until(
                EC.url_to_be(
                    expected_delete_url
                )
            )

        confirmation_form = self.wait.until(
            EC.visibility_of_element_located(
                self.DELETE_CONFIRMATION_FORM_LOCATOR
            )
        )

        self.assertIsNotNone(
            confirmation_form
        )

        return confirmation_form

    def wait_for_category_changelist(self):
        """
        Wait until Django Admin finishes loading and visibly
        renders the Category changelist.
        """
        expected_url = self.admin_url(
            self.CATEGORY_ADMIN_PATH
        )

        self.wait.until(
            EC.url_to_be(
                expected_url
            )
        )

        self.wait_for_document_ready()

        category_changelist = self.wait.until(
            EC.visibility_of_element_located(
                self.CATEGORY_CHANGELIST_LOCATOR
            )
        )

        self.assertIsNotNone(
            category_changelist
        )

        return category_changelist

    # =====================================================
    # ADMIN LOGIN HELPER
    # =====================================================

    def admin_login(self):
        """
        Log the Selenium browser into Django Admin and wait
        until the administration index is fully rendered.
        """
        self.open_path(
            self.ADMIN_LOGIN_PATH
        )

        username_input = self.wait.until(
            EC.element_to_be_clickable(
                self.USERNAME_LOCATOR
            )
        )

        username_input.clear()
        username_input.send_keys(
            self.ADMIN_USERNAME
        )

        password_input = self.wait.until(
            EC.element_to_be_clickable(
                self.PASSWORD_LOCATOR
            )
        )

        password_input.clear()
        password_input.send_keys(
            self.ADMIN_PASSWORD
        )

        self.safe_click(
            self.ADMIN_LOGIN_SUBMIT_LOCATOR
        )

        expected_admin_url = self.admin_url(
            self.ADMIN_INDEX_PATH
        )

        self.wait.until(
            EC.url_to_be(expected_admin_url)
        )

        self.wait_for_admin_content()

        self.wait.until(
            lambda driver:
            "Site administration"
            in driver.page_source
        )

        self.assertEqual(
            self.browser.current_url,
            expected_admin_url,
        )

        self.assertIn(
            "Site administration",
            self.browser.page_source,
        )

    # =====================================================
    # PRODUCT CREATION HELPER
    # =====================================================

    def create_product_through_admin(self):
        """
        Create the standard Selenium Product through the
        Django Admin browser interface.
        """
        self.open_path(
            self.PRODUCT_ADD_PATH
        )

        self.wait_for_product_form()

        # Category
        category_element = self.wait.until(
            EC.element_to_be_clickable(
                self.CATEGORY_FIELD_LOCATOR
            )
        )

        category_select = Select(
            category_element
        )

        category_select.select_by_value(
            str(self.category.pk)
        )

        # Product name
        name_input = self.wait.until(
            EC.element_to_be_clickable(
                self.NAME_FIELD_LOCATOR
            )
        )

        name_input.clear()
        name_input.send_keys(
            self.PRODUCT_NAME
        )

        # Description
        description_input = self.wait.until(
            EC.element_to_be_clickable(
                self.DESCRIPTION_FIELD_LOCATOR
            )
        )

        description_input.clear()
        description_input.send_keys(
            "Product created by Selenium "
            "for automated browser testing."
        )

        # Condition
        condition_element = self.wait.until(
            EC.element_to_be_clickable(
                self.CONDITION_FIELD_LOCATOR
            )
        )

        condition_select = Select(
            condition_element
        )

        condition_select.select_by_value(
            Product.Condition.NEW
        )

        # SGnG price
        price_input = self.wait.until(
            EC.element_to_be_clickable(
                self.SGNG_PRICE_FIELD_LOCATOR
            )
        )

        price_input.clear()
        price_input.send_keys(
            "39.99"
        )

        # Reference price
        reference_price_input = self.wait.until(
            EC.element_to_be_clickable(
                self.REFERENCE_PRICE_FIELD_LOCATOR
            )
        )

        reference_price_input.clear()
        reference_price_input.send_keys(
            "59.99"
        )

        # Inventory
        inventory_input = self.wait.until(
            EC.element_to_be_clickable(
                self.INVENTORY_FIELD_LOCATOR
            )
        )

        inventory_input.clear()
        inventory_input.send_keys(
            "2"
        )

        # Active normally defaults to True. Ensure that the
        # checkbox remains selected.
        active_checkbox = self.wait.until(
            EC.presence_of_element_located(
                self.ACTIVE_FIELD_LOCATOR
            )
        )

        if not active_checkbox.is_selected():
            self.safe_click(
                self.ACTIVE_FIELD_LOCATOR
            )

        # Save the Product.
        self.safe_click(
            self.SAVE_BUTTON_LOCATOR
        )

        # Wait for Django Admin to complete the database write
        # and redirect to the exact Product changelist.
        self.wait_for_product_changelist()

        product = Product.objects.get(
            name=self.PRODUCT_NAME
        )

        return product

    # =====================================================
    # PRODUCT ADMIN ACCESS
    # =====================================================

    def test_superuser_can_open_product_admin(self):
        """
        A superuser can log in to Django Admin, open the
        Catalog Products section, and reach the Product
        changelist.
        """
        self.admin_login()

        self.assertIn(
            "Site administration",
            self.browser.page_source,
        )

        self.assertIn(
            "Products",
            self.browser.page_source,
        )

        self.safe_click(
            self.PRODUCTS_LINK_LOCATOR
        )

        product_changelist = (
            self.wait_for_product_changelist()
        )

        self.assertIsNotNone(
            product_changelist
        )

        self.assertEqual(
            self.browser.current_url,
            self.admin_url(
                self.PRODUCT_ADMIN_PATH
            ),
        )

    # =====================================================
    # CREATE PRODUCT
    # =====================================================

    def test_superuser_can_create_product(self):
        """
        A superuser can create a Marketplace Product through
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

        product_changelist = self.wait.until(
            EC.presence_of_element_located(
                self.PRODUCT_CHANGELIST_LOCATOR
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

        product_change_path = (
            f"/admin/catalog/product/"
            f"{product.pk}/change/"
        )

        self.open_path(
            product_change_path
        )

        self.wait_for_product_form()

        name_input = self.wait.until(
            EC.element_to_be_clickable(
                self.NAME_FIELD_LOCATOR
            )
        )

        name_input.clear()
        name_input.send_keys(
            self.UPDATED_PRODUCT_NAME
        )

        price_input = self.wait.until(
            EC.element_to_be_clickable(
                self.SGNG_PRICE_FIELD_LOCATOR
            )
        )

        price_input.clear()
        price_input.send_keys(
            "34.99"
        )

        inventory_input = self.wait.until(
            EC.element_to_be_clickable(
                self.INVENTORY_FIELD_LOCATOR
            )
        )

        inventory_input.clear()
        inventory_input.send_keys(
            "5"
        )

        self.safe_click(
            self.SAVE_BUTTON_LOCATOR
        )

        # The change-form URL already contains the Product Admin
        # path, so wait for the exact changelist URL rather than
        # using url_contains().
        product_changelist = (
            self.wait_for_product_changelist()
        )

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

        product_delete_path = (
            f"/admin/catalog/product/"
            f"{product_pk}/delete/"
        )

        self.open_path(
            product_delete_path
        )

        expected_delete_url = self.admin_url(
            product_delete_path
        )

        confirmation_form = (
            self.wait_for_delete_confirmation(
                expected_delete_url
            )
        )

        self.assertIsNotNone(
            confirmation_form
        )

        self.assertIn(
            self.PRODUCT_NAME,
            self.browser.page_source,
        )

        # Confirm that the Product still exists before deletion.
        self.assertTrue(
            Product.objects.filter(
                pk=product_pk
            ).exists()
        )

        # Submit the Django Admin confirmation form.
        self.safe_click(
            self.DELETE_CONFIRMATION_BUTTON_LOCATOR
        )

        # After deletion, Django Admin should redirect to the
        # Product changelist.
        product_changelist = (
            self.wait_for_product_changelist()
        )

        # Verify persistent deletion from the test database.
        self.assertFalse(
            Product.objects.filter(
                pk=product_pk
            ).exists()
        )

        self.assertIsNotNone(
            product_changelist
        )

        # Verify that no Product row in the rendered changelist
        # contains the deleted Product name. The Django Admin
        # success message may still contain the name.
        product_result_links = self.browser.find_elements(
            By.CSS_SELECTOR,
            "#result_list tbody th a, "
            "#result_list tbody td a",
        )

        rendered_product_names = [
            link.text.strip()
            for link in product_result_links
            if link.text.strip()
        ]

        self.assertNotIn(
            self.PRODUCT_NAME,
            rendered_product_names,
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

        product_change_path = (
            f"/admin/catalog/product/"
            f"{product.pk}/change/"
        )

        self.open_path(
            product_change_path
        )

        self.wait_for_product_form()

        inventory_input = self.wait.until(
            EC.element_to_be_clickable(
                self.INVENTORY_FIELD_LOCATOR
            )
        )

        inventory_input.clear()
        inventory_input.send_keys(
            "0"
        )

        self.safe_click(
            self.SAVE_BUTTON_LOCATOR
        )

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

        self.open_path(
            self.CATEGORY_ADMIN_PATH
        )

        category_changelist = (
            self.wait_for_category_changelist()
        )

        self.assertIsNotNone(
            category_changelist
        )

        self.assertIn(
            self.category.name,
            self.browser.page_source,
        )
        