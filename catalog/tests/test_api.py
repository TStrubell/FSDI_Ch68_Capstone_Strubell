from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Category, Product


class CatalogApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Outdoor Gear",
            description="Outdoor equipment.",
            active=True,
        )

        cls.product = Product.objects.create(
            category=cls.category,
            name="SGnG Trail Backpack",
            description=(
                "A practical trail backpack "
                "for outdoor use."
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

        cls.inactive_product = Product.objects.create(
            category=cls.category,
            name="Inactive Product",
            description=(
                "This product must not appear "
                "in the public API."
            ),
            condition=Product.Condition.NEW,
            sgng_price=Decimal("20.00"),
            inventory_quantity=1,
            featured=False,
            active=False,
        )

    # =====================================================
    # CATEGORIES
    # =====================================================

    def test_category_list_returns_200(self):
        response = self.client.get(
            reverse(
                "catalog-api:category-list"
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_category_list_contains_category(self):
        response = self.client.get(
            reverse(
                "catalog-api:category-list"
            )
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["name"],
            "Outdoor Gear",
        )

    def test_category_detail_uses_slug(self):
        response = self.client.get(
            reverse(
                "catalog-api:category-detail",
                kwargs={
                    "slug": (
                        self.category.slug
                    ),
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["slug"],
            "outdoor-gear",
        )

    def test_category_product_count(self):
        response = self.client.get(
            reverse(
                "catalog-api:category-detail",
                kwargs={
                    "slug": (
                        self.category.slug
                    ),
                },
            )
        )

        self.assertEqual(
            response.data[
                "product_count"
            ],
            1,
        )

    # =====================================================
    # PRODUCTS
    # =====================================================

    def test_product_list_returns_200(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-list"
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_product_list_contains_active_product(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-list"
            )
        )

        names = [
            product["name"]
            for product
            in response.data
        ]

        self.assertIn(
            self.product.name,
            names,
        )

    def test_product_list_hides_inactive_product(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-list"
            )
        )

        names = [
            product["name"]
            for product
            in response.data
        ]

        self.assertNotIn(
            self.inactive_product.name,
            names,
        )

    def test_product_detail_returns_200(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-detail",
                kwargs={
                    "slug": (
                        self.product.slug
                    ),
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_product_detail_contains_expected_data(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-detail",
                kwargs={
                    "slug": (
                        self.product.slug
                    ),
                },
            )
        )

        self.assertEqual(
            response.data["name"],
            "SGnG Trail Backpack",
        )

        self.assertEqual(
            response.data[
                "category_name"
            ],
            "Outdoor Gear",
        )

        self.assertEqual(
            response.data[
                "category_slug"
            ],
            "outdoor-gear",
        )

        self.assertEqual(
            response.data[
                "condition"
            ],
            "gently_used",
        )

        self.assertEqual(
            response.data[
                "condition_display"
            ],
            "Gently Used",
        )

    def test_product_savings_are_correct(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-detail",
                kwargs={
                    "slug": self.product.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["savings_amount"],
            "30.00",
        )

        self.assertEqual(
            response.data["savings_percentage"],
            37,
        )

    def test_product_availability_is_correct(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-detail",
                kwargs={
                    "slug": (
                        self.product.slug
                    ),
                },
            )
        )

        self.assertTrue(
            response.data[
                "is_available"
            ]
        )

    # =====================================================
    # API FILTERS
    # =====================================================

    def test_category_filter(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-list"
            ),
            {
                "category":
                    "outdoor-gear",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_condition_filter(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-list"
            ),
            {
                "condition":
                    "gently_used",
            },
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["name"],
            self.product.name,
        )

    def test_featured_filter(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-list"
            ),
            {
                "featured": "true",
            },
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertTrue(
            response.data[0][
                "featured"
            ]
        )

    def test_search(self):
        response = self.client.get(
            reverse(
                "catalog-api:product-list"
            ),
            {
                "search": "Backpack",
            },
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["name"],
            self.product.name,
        )

    # =====================================================
    # READ-ONLY SECURITY
    # =====================================================

    def test_product_post_not_allowed(self):
        response = self.client.post(
            reverse(
                "catalog-api:product-list"
            ),
            data={
                "name":
                    "Unauthorized Product",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_category_post_not_allowed(self):
        response = self.client.post(
            reverse(
                "catalog-api:category-list"
            ),
            data={
                "name":
                    "Unauthorized Category",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )