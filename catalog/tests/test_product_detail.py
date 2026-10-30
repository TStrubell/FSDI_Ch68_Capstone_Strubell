from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


class ProductDetailTests(TestCase):
    """Tests the SGnG Product Detail page."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Outdoor Gear",
        )

        cls.product = Product.objects.create(
            category=cls.category,
            name="SGnG Trail Backpack",
            description=(
                "A versatile gently used backpack "
                "for hiking and everyday use."
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

        cls.inactive_product = (
            Product.objects.create(
                category=cls.category,
                name="Unavailable Test Product",
                description=(
                    "Inactive product."
                ),
                condition=Product.Condition.NEW,
                sgng_price=Decimal("20.00"),
                inventory_quantity=1,
                active=False,
            )
        )

    def test_product_detail_returns_200(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_product_detail_uses_correct_template(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )

        self.assertTemplateUsed(
            response,
            "catalog/product_detail.html",
        )

    def test_product_detail_contains_name(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )

        self.assertContains(
            response,
            self.product.name,
        )

    def test_product_detail_contains_description(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )

        self.assertContains(
            response,
            (
                "A versatile gently used "
                "backpack"
            ),
        )

    def test_product_detail_contains_sgng_price(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )

        self.assertContains(
            response,
            "49.99",
        )

    def test_product_detail_contains_reference_price(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )

        self.assertContains(
            response,
            "79.99",
        )

    def test_product_detail_contains_condition(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )

        self.assertContains(
            response,
            "Gently Used",
        )

    def test_product_detail_contains_inventory(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )

        self.assertContains(
            response,
            "In Stock",
        )

    def test_product_savings_amount(self):
        self.assertEqual(
            self.product.savings_amount,
            Decimal("30.00"),
        )

    def test_product_savings_percentage(self):
        self.assertEqual(
            self.product.savings_percentage,
            Decimal("37.50"),
        )

    def test_product_is_available(self):
        self.assertTrue(
            self.product.is_available
        )

    def test_zero_inventory_is_unavailable(self):
        self.product.inventory_quantity = 0

        self.product.save(
            update_fields=[
                "inventory_quantity"
            ]
        )

        self.assertFalse(
            self.product.is_available
        )

    def test_inactive_product_returns_404(self):
        response = self.client.get(
            reverse(
                "catalog:product-detail",
                kwargs={
                    "slug": (
                        self.inactive_product.slug
                    )
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )