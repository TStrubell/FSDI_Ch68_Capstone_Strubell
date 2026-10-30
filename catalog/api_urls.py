from django.db.models import Q
from django.urls import path

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
)


# =========================================================
# CATEGORY API VIEWS
# =========================================================


class CategoryListAPIView(ListAPIView):
    """
    Return all active SGnG marketplace categories.

    Optional query parameters:

    ?search=outdoor
    ?ordering=name
    ?ordering=-created_at
    """

    serializer_class = CategorySerializer

    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        queryset = (
            Category.objects
            .filter(active=True)
            .order_by("name")
        )

        search_query = (
            self.request.query_params
            .get("search", "")
            .strip()
        )

        ordering = (
            self.request.query_params
            .get("ordering", "name")
            .strip()
        )

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(
                    description__icontains=
                    search_query
                )
            )

        allowed_ordering = {
            "name",
            "-name",
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
        }

        if ordering in allowed_ordering:
            queryset = queryset.order_by(
                ordering,
            )

        return queryset


class CategoryDetailAPIView(RetrieveAPIView):
    """
    Return one active category using its slug.
    """

    serializer_class = CategorySerializer

    permission_classes = [
        AllowAny,
    ]

    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.filter(
            active=True,
        )


# =========================================================
# PRODUCT API VIEWS
# =========================================================


class ProductListAPIView(ListAPIView):
    """
    Return all active products in active categories.

    Supported query parameters:

    ?search=backpack
    ?category=outdoor-gear
    ?condition=gently_used
    ?featured=true
    ?ordering=sgng_price
    ?ordering=-sgng_price
    """

    serializer_class = ProductSerializer

    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        queryset = (
            Product.objects
            .select_related("category")
            .filter(
                active=True,
                category__active=True,
            )
            .order_by(
                "-featured",
                "-created_at",
            )
        )

        search_query = (
            self.request.query_params
            .get("search", "")
            .strip()
        )

        category_slug = (
            self.request.query_params
            .get("category", "")
            .strip()
        )

        condition = (
            self.request.query_params
            .get("condition", "")
            .strip()
        )

        featured = (
            self.request.query_params
            .get("featured", "")
            .strip()
            .lower()
        )

        ordering = (
            self.request.query_params
            .get("ordering", "")
            .strip()
        )

        # Search by product name, description,
        # or category name.
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(
                    description__icontains=
                    search_query
                )
                | Q(
                    category__name__icontains=
                    search_query
                )
            )

        # Filter by Category slug.
        if category_slug:
            queryset = queryset.filter(
                category__slug=category_slug,
            )

        # Validate and apply Condition filtering.
        valid_conditions = {
            value
            for value, label
            in Product.Condition.choices
        }

        if condition in valid_conditions:
            queryset = queryset.filter(
                condition=condition,
            )

        # Filter by Featured status.
        true_values = {
            "true",
            "1",
            "yes",
        }

        false_values = {
            "false",
            "0",
            "no",
        }

        if featured in true_values:
            queryset = queryset.filter(
                featured=True,
            )

        elif featured in false_values:
            queryset = queryset.filter(
                featured=False,
            )

        # Restrict ordering to known model fields.
        allowed_ordering = {
            "name",
            "-name",
            "sgng_price",
            "-sgng_price",
            "reference_price",
            "-reference_price",
            "inventory_quantity",
            "-inventory_quantity",
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
        }

        if ordering in allowed_ordering:
            queryset = queryset.order_by(
                ordering,
            )

        return queryset


class ProductDetailAPIView(RetrieveAPIView):
    """
    Return one active product using its slug.
    """

    serializer_class = ProductSerializer

    permission_classes = [
        AllowAny,
    ]

    lookup_field = "slug"

    def get_queryset(self):
        return (
            Product.objects
            .select_related("category")
            .filter(
                active=True,
                category__active=True,
            )
        )


# =========================================================
# API URL PATTERNS
# =========================================================


app_name = "catalog-api"


urlpatterns = [
    # Categories
    path(
        "categories/",
        CategoryListAPIView.as_view(),
        name="category-list",
    ),

    path(
        "categories/<slug:slug>/",
        CategoryDetailAPIView.as_view(),
        name="category-detail",
    ),

    # Products
    path(
        "products/",
        ProductListAPIView.as_view(),
        name="product-list",
    ),

    path(
        "products/<slug:slug>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
]