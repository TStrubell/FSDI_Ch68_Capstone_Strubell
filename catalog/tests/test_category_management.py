from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


User = get_user_model()


class CategoryManagementTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = User.objects.create_user(
            username="category_staff",
            email="category.staff@example.com",
            password="StrongTestPassword123!",
            is_staff=True,
        )

        cls.normal_user = User.objects.create_user(
            username="category_customer",
            email="category.customer@example.com",
            password="StrongTestPassword123!",
        )

        cls.outdoor = Category.objects.create(
            name="Outdoor Gear",
            description="Outdoor equipment and trail gear.",
            active=True,
        )

        cls.unused = Category.objects.create(
            name="Camp Kitchen",
            description="Camp cooking equipment.",
            active=True,
        )

        cls.product = Product.objects.create(
            category=cls.outdoor,
            name="Trail Test Pack",
            description="A test Product assigned to Outdoor Gear.",
            condition=Product.Condition.NEW,
            sgng_price="49.99",
            reference_price="69.99",
            inventory_quantity=4,
            active=True,
        )

    def setUp(self):
        self.list_url = reverse(
            "catalog:category-management"
        )

        self.create_url = reverse(
            "catalog:category-create"
        )

        self.update_url = reverse(
            "catalog:category-update",
            kwargs={"pk": self.outdoor.pk},
        )

        self.protected_delete_url = reverse(
            "catalog:category-delete",
            kwargs={"pk": self.outdoor.pk},
        )

        self.unused_delete_url = reverse(
            "catalog:category-delete",
            kwargs={"pk": self.unused.pk},
        )

    def test_anonymous_user_is_redirected_from_category_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse("accounts:login"),
            response.url,
        )

    def test_non_staff_user_cannot_access_category_list(self):
        self.client.force_login(self.normal_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 403)

    def test_staff_user_can_access_category_list(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/category_management.html",
        )
        self.assertContains(
            response,
            self.outdoor.name,
        )
        self.assertContains(
            response,
            self.unused.name,
        )

    def test_category_list_includes_product_count(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.list_url)

        category = next(
            category
            for category in response.context["categories"]
            if category.pk == self.outdoor.pk
        )

        self.assertEqual(category.product_count, 1)

    def test_staff_user_can_create_category(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            self.create_url,
            data={
                "name": "Trail Accessories",
                "description": (
                    "Accessories for trail travel."
                ),
                "active": True,
            },
        )

        self.assertRedirects(
            response,
            self.list_url,
        )

        category = Category.objects.get(
            name="Trail Accessories"
        )

        self.assertEqual(
            category.slug,
            "trail-accessories",
        )
        self.assertTrue(category.active)

    def test_duplicate_category_name_is_rejected(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            self.create_url,
            data={
                "name": "Outdoor Gear",
                "description": "Duplicate name.",
                "active": True,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "name",
            "Category with this Name already exists.",
        )

    def test_staff_user_can_update_category(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            self.update_url,
            data={
                "name": "Outdoor Equipment",
                "description": (
                    "Updated outdoor equipment description."
                ),
                "active": False,
            },
        )

        self.assertRedirects(
            response,
            self.list_url,
        )

        self.outdoor.refresh_from_db()

        self.assertEqual(
            self.outdoor.name,
            "Outdoor Equipment",
        )
        self.assertFalse(self.outdoor.active)

    def test_category_with_products_cannot_be_deleted(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            self.protected_delete_url,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Category.objects.filter(
                pk=self.outdoor.pk
            ).exists()
        )
        self.assertContains(
            response,
            "cannot be deleted",
        )

    def test_unused_category_can_be_deleted(self):
        self.client.force_login(self.staff_user)

        unused_pk = self.unused.pk

        response = self.client.post(
            self.unused_delete_url,
        )

        self.assertRedirects(
            response,
            self.list_url,
        )
        self.assertFalse(
            Category.objects.filter(
                pk=unused_pk
            ).exists()
        )

    def test_inactive_category_is_hidden_from_marketplace(self):
        self.outdoor.active = False
        self.outdoor.save()

        response = self.client.get(
            reverse("catalog:product-list")
        )

        self.assertNotContains(
            response,
            self.product.name,
        )