from decimal import Decimal

from django.test import TestCase

from django.urls import reverse

from catalog.models import (
    Category,
    Product,
)


class CatalogViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.outdoor = (
            Category.objects.create(
                name="Outdoor Gear",
                active=True,
            )
        )

        cls.tools = (
            Category.objects.create(
                name="Tools",
                active=True,
            )
        )

        cls.backpack = (
            Product.objects.create(
                category=cls.outdoor,
                name=(
                    "SGnG Trail Backpack"
                ),
                description=(
                    "A practical "
                    "trail backpack."
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

        cls.multi_tool = (
            Product.objects.create(
                category=cls.tools,
                name=(
                    "Compact Outdoor "
                    "Multi-Tool"
                ),
                description=(
                    "A compact "
                    "outdoor tool."
                ),
                condition=(
                    Product.Condition.NEW
                ),
                sgng_price=(
                    Decimal("29.99")
                ),
                reference_price=(
                    Decimal("39.99")
                ),
                inventory_quantity=6,
                featured=True,
                active=True,
            )
        )

        cls.inactive_product = (
            Product.objects.create(
                category=cls.tools,
                name="Inactive Product",
                description=(
                    "Not publicly visible."
                ),
                condition=(
                    Product.Condition.NEW
                ),
                sgng_price=(
                    Decimal("10.00")
                ),
                inventory_quantity=1,
                active=False,
            )
        )

    def test_marketplace_returns_200(self):
        response = self.client.get(
            reverse(
                "catalog:product-list"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_marketplace_uses_template(self):
        response = self.client.get(
            reverse(
                "catalog:product-list"
            )
        )

        self.assertTemplateUsed(
            response,
            "catalog/product_list.html",
        )

    def test_active_products_display(self):
        response = self.client.get(
            reverse(
                "catalog:product-list"
            )
        )

        self.assertContains(
            response,
            self.backpack.name,
        )

        self.assertContains(
            response,
            self.multi_tool.name,
        )

    def test_inactive_product_hidden(self):
        response = self.client.get(
            reverse(
                "catalog:product-list"
            )
        )

        self.assertNotContains(
            response,
            self.inactive_product.name,
        )

    def test_search_filter(self):
        response = self.client.get(
            reverse(
                "catalog:product-list"
            ),
            {
                "q": "Backpack",
            },
        )

        self.assertContains(
            response,
            self.backpack.name,
        )

        self.assertNotContains(
            response,
            self.multi_tool.name,
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse(
                "catalog:product-list"
            ),
            {
                "category":
                self.tools.slug,
            },
        )

        self.assertContains(
            response,
            self.multi_tool.name,
        )

        self.assertNotContains(
            response,
            self.backpack.name,
        )

    def test_condition_filter(self):
        response = self.client.get(
            reverse(
                "catalog:product-list"
            ),
            {
                "condition":
                Product.Condition
                .GENTLY_USED,
            },
        )

        self.assertContains(
            response,
            self.backpack.name,
        )

        self.assertNotContains(
            response,
            self.multi_tool.name,
        )

    def test_product_detail_returns_200(self):
        response = self.client.get(
            self.backpack
            .get_absolute_url()
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_product_detail_template(self):
        response = self.client.get(
            self.backpack
            .get_absolute_url()
        )

        self.assertTemplateUsed(
            response,
            (
                "catalog/"
                "product_detail.html"
            ),
        )

    def test_product_detail_content(self):
        response = self.client.get(
            self.backpack
            .get_absolute_url()
        )

        self.assertContains(
            response,
            self.backpack.name,
        )

        self.assertContains(
            response,
            "49.99",
        )

        self.assertContains(
            response,
            "30.00",
        )

    def test_inactive_detail_returns_404(self):
        response = self.client.get(
            self.inactive_product
            .get_absolute_url()
        )

        self.assertEqual(
            response.status_code,
            404,
        )