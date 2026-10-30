from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


class HomePageTests(TestCase):
    """Tests the Cinematic SGnG Homepage."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Outdoor Gear",
            description=(
                "Outdoor products for testing."
            ),
        )

        cls.featured_product = Product.objects.create(
            category=cls.category,
            name="Featured Trail Backpack",
            description=(
                "A featured test backpack."
            ),
            condition=(
                Product.Condition.GENTLY_USED
            ),
            sgng_price=Decimal("49.99"),
            reference_price=Decimal("79.99"),
            inventory_quantity=2,
            featured=True,
            active=True,
        )

        cls.regular_product = Product.objects.create(
            category=cls.category,
            name="Regular Marketplace Product",
            description=(
                "A non-featured product."
            ),
            condition=Product.Condition.NEW,
            sgng_price=Decimal("20.00"),
            inventory_quantity=3,
            featured=False,
            active=True,
        )

        cls.inactive_featured_product = (
            Product.objects.create(
                category=cls.category,
                name="Inactive Featured Product",
                description=(
                    "This product should not appear."
                ),
                condition=Product.Condition.NEW,
                sgng_price=Decimal("30.00"),
                inventory_quantity=1,
                featured=True,
                active=False,
            )
        )

    def setUp(self):
        self.url = reverse(
            "pages:home"
        )

    def test_homepage_returns_200(self):
        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_homepage_uses_correct_template(self):
        response = self.client.get(
            self.url
        )

        self.assertTemplateUsed(
            response,
            "pages/home.html",
        )

    def test_homepage_has_featured_products_context(self):
        response = self.client.get(
            self.url
        )

        self.assertIn(
            "featured_products",
            response.context,
        )

    def test_homepage_displays_featured_product(self):
        response = self.client.get(
            self.url
        )

        self.assertContains(
            response,
            self.featured_product.name,
        )

    def test_homepage_hides_nonfeatured_product(self):
        response = self.client.get(
            self.url
        )

        self.assertNotContains(
            response,
            self.regular_product.name,
        )

    def test_homepage_hides_inactive_featured_product(self):
        response = self.client.get(
            self.url
        )

        self.assertNotContains(
            response,
            self.inactive_featured_product.name,
        )

    def test_homepage_contains_marketplace_cta(self):
        response = self.client.get(
            self.url
        )

        self.assertContains(
            response,
            reverse(
                "catalog:product-list"
            ),
        )

    def test_homepage_contains_sgng_story(self):
        response = self.client.get(
            self.url
        )

        self.assertContains(
            response,
            "The SGnG Story",
        )

    def test_homepage_contains_story_topics(self):
        response = self.client.get(
            self.url
        )

        for topic in (
            "Military Service",
            "Craftsmanship",
            "Entrepreneurship",
            "Software Development",
        ):
            with self.subTest(
                topic=topic
            ):
                self.assertContains(
                    response,
                    topic,
                )


class AboutPageTests(TestCase):
    """Tests the SGnG About page."""

    def test_about_returns_200(self):
        response = self.client.get(
            reverse("pages:about")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_about_uses_correct_template(self):
        response = self.client.get(
            reverse("pages:about")
        )

        self.assertTemplateUsed(
            response,
            "pages/about.html",
        )