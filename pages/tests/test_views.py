from decimal import Decimal

from django.test import TestCase

from django.urls import reverse

from catalog.models import (
    Category,
    Product,
)


class HomeViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        category = (
            Category.objects.create(
                name="Outdoor Gear",
                active=True,
            )
        )

        cls.featured = (
            Product.objects.create(
                category=category,
                name=(
                    "Featured Backpack"
                ),
                description=(
                    "Featured product."
                ),
                condition=(
                    Product.Condition.NEW
                ),
                sgng_price=(
                    Decimal("49.99")
                ),
                inventory_quantity=1,
                featured=True,
                active=True,
            )
        )

        cls.not_featured = (
            Product.objects.create(
                category=category,
                name="Regular Product",
                description=(
                    "Not featured."
                ),
                condition=(
                    Product.Condition.NEW
                ),
                sgng_price=(
                    Decimal("19.99")
                ),
                inventory_quantity=2,
                featured=False,
                active=True,
            )
        )

        cls.inactive_featured = (
            Product.objects.create(
                category=category,
                name=(
                    "Inactive Featured"
                ),
                description=(
                    "Should not display."
                ),
                condition=(
                    Product.Condition.NEW
                ),
                sgng_price=(
                    Decimal("15.00")
                ),
                inventory_quantity=1,
                featured=True,
                active=False,
            )
        )

    def test_home_returns_200(self):
        response = self.client.get(
            reverse("pages:home")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_home_template(self):
        response = self.client.get(
            reverse("pages:home")
        )

        self.assertTemplateUsed(
            response,
            "pages/home.html",
        )

    def test_featured_product_visible(self):
        response = self.client.get(
            reverse("pages:home")
        )

        self.assertContains(
            response,
            self.featured.name,
        )

    def test_nonfeatured_hidden(self):
        response = self.client.get(
            reverse("pages:home")
        )

        self.assertNotContains(
            response,
            self.not_featured.name,
        )

    def test_inactive_featured_hidden(self):
        response = self.client.get(
            reverse("pages:home")
        )

        self.assertNotContains(
            response,
            self.inactive_featured.name,
        )


class AboutViewTests(TestCase):

    def test_about_returns_200(self):
        response = self.client.get(
            reverse("pages:about")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_about_template(self):
        response = self.client.get(
            reverse("pages:about")
        )

        self.assertTemplateUsed(
            response,
            "pages/about.html",
        )