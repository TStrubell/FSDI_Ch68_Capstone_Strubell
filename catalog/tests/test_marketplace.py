from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


class MarketplaceTests(TestCase):
    """Tests the SGnG Marketplace catalog."""

    @classmethod
    def setUpTestData(cls):
        cls.outdoor = Category.objects.create(
            name="Outdoor Gear",
        )

        cls.tools = Category.objects.create(
            name="Tools",
        )

        cls.backpack = Product.objects.create(
            category=cls.outdoor,
            name="SGnG Trail Backpack",
            description=(
                "A versatile backpack for outdoor use."
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

        cls.multi_tool = Product.objects.create(
            category=cls.tools,
            name="Compact Outdoor Multi-Tool",
            description=(
                "A compact tool for outdoor activities."
            ),
            condition=Product.Condition.NEW,
            sgng_price=Decimal("29.99"),
            reference_price=Decimal("39.99"),
            inventory_quantity=6,
            featured=False,
            active=True,
        )

        cls.inactive_product = (
            Product.objects.create(
                category=cls.tools,
                name="Inactive Product",
                description=(
                    "This product is not public."
                ),
                condition=Product.Condition.NEW,
                sgng_price=Decimal("9.99"),
                inventory_quantity=1,
                active=False,
            )
        )

    def setUp(self):
        self.url = reverse(
            "catalog:product-list"
        )

    def test_marketplace_returns_200(self):
        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_marketplace_uses_correct_template(self):
        response = self.client.get(
            self.url
        )

        self.assertTemplateUsed(
            response,
            "catalog/product_list.html",
        )

    def test_active_products_are_displayed(self):
        response = self.client.get(
            self.url
        )

        self.assertContains(
            response,
            self.backpack.name,
        )

        self.assertContains(
            response,
            self.multi_tool.name,
        )

    def test_inactive_product_is_hidden(self):
        response = self.client.get(
            self.url
        )

        self.assertNotContains(
            response,
            self.inactive_product.name,
        )

    def test_search_by_product_name(self):
        response = self.client.get(
            self.url,
            {"q": "Backpack"},
        )

        self.assertContains(
            response,
            self.backpack.name,
        )

        self.assertNotContains(
            response,
            self.multi_tool.name,
        )

    def test_search_by_category_name(self):
        response = self.client.get(
            self.url,
            {"q": "Tools"},
        )

        self.assertContains(
            response,
            self.multi_tool.name,
        )

        self.assertNotContains(
            response,
            self.backpack.name,
        )

    def test_no_search_results_shows_empty_state(self):
        response = self.client.get(
            self.url,
            {
                "q": (
                    "this-product-does-not-exist"
                )
            },
        )

        self.assertContains(
            response,
            "No Products Found",
        )

    def test_filter_by_category(self):
        response = self.client.get(
            self.url,
            {
                "category": (
                    self.outdoor.slug
                )
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

    def test_filter_by_condition(self):
        response = self.client.get(
            self.url,
            {
                "condition": (
                    Product.Condition.GENTLY_USED
                )
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

    def test_sort_price_low_to_high(self):
        response = self.client.get(
            self.url,
            {
                "sort": "price_low",
            },
        )

        products = list(
            response.context["products"]
        )

        self.assertEqual(
            products[0],
            self.multi_tool,
        )

        self.assertEqual(
            products[1],
            self.backpack,
        )

    def test_sort_price_high_to_low(self):
        response = self.client.get(
            self.url,
            {
                "sort": "price_high",
            },
        )

        products = list(
            response.context["products"]
        )

        self.assertEqual(
            products[0],
            self.backpack,
        )

        self.assertEqual(
            products[1],
            self.multi_tool,
        )

    def test_categories_are_in_context(self):
        response = self.client.get(
            self.url
        )

        self.assertIn(
            "categories",
            response.context,
        )

        categories = list(
            response.context["categories"]
        )

        self.assertIn(
            self.outdoor,
            categories,
        )

        self.assertIn(
            self.tools,
            categories,
        )