from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


User = get_user_model()


class StaffProductCRUDTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Outdoor Gear",
            description="Outdoor equipment.",
            active=True,
        )

        cls.product = Product.objects.create(
            category=cls.category,
            name="Existing Product",
            description=(
                "An existing marketplace product."
            ),
            condition=Product.Condition.NEW,
            sgng_price=Decimal("20.00"),
            reference_price=Decimal("30.00"),
            inventory_quantity=2,
            featured=False,
            active=True,
        )

        cls.normal_user = User.objects.create_user(
            username="normaluser",
            email="normal@example.com",
            password="StrongTestPassword123!",
        )

        cls.staff_user = User.objects.create_user(
            username="staffuser",
            email="staff@example.com",
            password="StrongTestPassword123!",
            is_staff=True,
        )

    def setUp(self):
        self.management_url = reverse(
            "catalog:product-management"
        )

        self.create_url = reverse(
            "catalog:product-create"
        )

        self.update_url = reverse(
            "catalog:product-update",
            kwargs={
                "pk": self.product.pk,
            },
        )

        self.delete_url = reverse(
            "catalog:product-delete",
            kwargs={
                "pk": self.product.pk,
            },
        )

    # =====================================================
    # ACCESS CONTROL
    # =====================================================

    def test_anonymous_user_cannot_access_create(self):
        response = self.client.get(
            self.create_url
        )

        self.assertNotEqual(
            response.status_code,
            200,
        )

    def test_normal_user_cannot_access_create(self):
        self.client.force_login(
            self.normal_user
        )

        response = self.client.get(
            self.create_url
        )

        self.assertNotEqual(
            response.status_code,
            200,
        )

    def test_staff_user_can_access_create(self):
        self.client.force_login(
            self.staff_user
        )

        response = self.client.get(
            self.create_url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "catalog/product_form.html",
        )

    def test_staff_user_can_access_update(self):
        self.client.force_login(
            self.staff_user
        )

        response = self.client.get(
            self.update_url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "catalog/product_form.html",
        )

    def test_staff_user_can_access_delete_confirmation(
        self,
    ):
        self.client.force_login(
            self.staff_user
        )

        response = self.client.get(
            self.delete_url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            (
                "catalog/"
                "product_confirm_delete.html"
            ),
        )

        self.assertContains(
            response,
            self.product.name,
        )

        self.assertContains(
            response,
            "Permanently Delete Product",
        )

    # =====================================================
    # CREATE
    # =====================================================

    def test_staff_user_can_create_product(self):
        self.client.force_login(
            self.staff_user
        )

        response = self.client.post(
            self.create_url,
            data={
                "category":
                    self.category.pk,
                "name":
                    "Created Product",
                "description":
                    "Created through Staff CRUD.",
                "condition":
                    Product.Condition.NEW,
                "sgng_price":
                    "34.99",
                "reference_price":
                    "49.99",
                "external_reference_url":
                    "",
                "inventory_quantity":
                    4,
                "featured":
                    True,
                "active":
                    True,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            Product.objects.filter(
                name="Created Product"
            ).exists()
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def test_staff_user_can_update_product(self):
        self.client.force_login(
            self.staff_user
        )

        response = self.client.post(
            self.update_url,
            data={
                "category":
                    self.category.pk,
                "name":
                    "Updated Product",
                "description":
                    "Updated through Staff CRUD.",
                "condition":
                    Product.Condition.GENTLY_USED,
                "sgng_price":
                    "18.00",
                "reference_price":
                    "28.00",
                "external_reference_url":
                    "",
                "inventory_quantity":
                    3,
                "featured":
                    True,
                "active":
                    True,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.name,
            "Updated Product",
        )

        self.assertEqual(
            self.product.inventory_quantity,
            3,
        )

        self.assertTrue(
            self.product.featured
        )

    # =====================================================
    # DELETE
    # =====================================================

    def test_staff_user_can_delete_product(self):
        self.client.force_login(
            self.staff_user
        )

        product_pk = self.product.pk

        response = self.client.post(
            self.delete_url
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            Product.objects.filter(
                pk=product_pk
            ).exists()
        )