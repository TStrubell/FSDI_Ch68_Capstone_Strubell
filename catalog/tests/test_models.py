from decimal import Decimal

from django.test import TestCase

from django.urls import reverse

from catalog.models import (
    Category,
    Product,
)


class CategoryModelTests(TestCase):

    def test_category_string(self):
        category = (
            Category.objects.create(
                name="Outdoor Gear",
            )
        )

        self.assertEqual(
            str(category),
            "Outdoor Gear",
        )

    def test_category_slug_generated(self):
        category = (
            Category.objects.create(
                name="Leather Goods",
            )
        )

        self.assertEqual(
            category.slug,
            "leather-goods",
        )


class ProductModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = (
            Category.objects.create(
                name="Outdoor Gear",
            )
        )

        cls.product = (
            Product.objects.create(
                category=cls.category,
                name=(
                    "SGnG Trail Backpack"
                ),
                description=(
                    "A practical trail "
                    "backpack."
                ),
                condition=(
                    Product.Condition
                    .GENTLY_USED
                ),
                sgng_price=(
                    Decimal("49.99")
                ),
                reference_price=(
                    Decimal("79.99")
                ),
                inventory_quantity=1,
                featured=True,
                active=True,
            )
        )

    def test_product_string(self):
        self.assertEqual(
            str(self.product),
            "SGnG Trail Backpack",
        )

    def test_product_slug_generated(self):
        self.assertEqual(
            self.product.slug,
            "sgng-trail-backpack",
        )

    def test_product_absolute_url(self):
        self.assertEqual(
            self.product
            .get_absolute_url(),
            reverse(
                "catalog:product-detail",
                kwargs={
                    "slug":
                    self.product.slug,
                },
            ),
        )

    def test_product_available(self):
        self.assertTrue(
            self.product.is_available
        )

    def test_zero_inventory_unavailable(self):
        self.product.inventory_quantity = 0

        self.assertFalse(
            self.product.is_available
        )

    def test_inactive_product_unavailable(self):
        self.product.active = False

        self.assertFalse(
            self.product.is_available
        )

    def test_savings_amount(self):
        self.assertEqual(
            self.product.savings_amount,
            Decimal("30.00"),
        )

    def test_savings_percentage(self):
        self.assertEqual(
            self.product
            .savings_percentage,
            Decimal("37.50"),
        )

    def test_no_reference_price_gives_zero_savings(self):
        self.product.reference_price = None

        self.assertEqual(
            self.product.savings_amount,
            Decimal("0.00"),
        )

        self.assertEqual(
            self.product
            .savings_percentage,
            Decimal("0.00"),
        )