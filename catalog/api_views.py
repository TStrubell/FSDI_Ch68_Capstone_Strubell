from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
)


class CategoryViewSet(
    ReadOnlyModelViewSet
):
    serializer_class = CategorySerializer

    permission_classes = [
        AllowAny,
    ]

    lookup_field = "slug"

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "created_at",
        "updated_at",
    ]

    ordering = [
        "name",
    ]

    def get_queryset(self):
        return (
            Category.objects
            .filter(active=True)
            .order_by("name")
        )


class ProductViewSet(
    ReadOnlyModelViewSet
):
    serializer_class = ProductSerializer

    permission_classes = [
        AllowAny,
    ]

    lookup_field = "slug"

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "name",
        "description",
        "category__name",
    ]

    ordering_fields = [
        "name",
        "sgng_price",
        "reference_price",
        "inventory_quantity",
        "created_at",
        "updated_at",
    ]

    ordering = [
        "-featured",
        "-created_at",
    ]

    def get_queryset(self):
        queryset = (
            Product.objects
            .select_related("category")
            .filter(
                active=True,
                category__active=True,
            )
        )

        category = (
            self.request
            .query_params
            .get(
                "category",
                "",
            )
            .strip()
        )

        condition = (
            self.request
            .query_params
            .get(
                "condition",
                "",
            )
            .strip()
        )

        featured = (
            self.request
            .query_params
            .get(
                "featured",
                "",
            )
            .strip()
            .lower()
        )

        if category:
            queryset = (
                queryset.filter(
                    category__slug=category
                )
            )

        valid_conditions = {
            value
            for value, label
            in Product.Condition.choices
        }

        if condition in valid_conditions:
            queryset = (
                queryset.filter(
                    condition=condition
                )
            )

        if featured in {
            "true",
            "1",
            "yes",
        }:
            queryset = (
                queryset.filter(
                    featured=True
                )
            )

        elif featured in {
            "false",
            "0",
            "no",
        }:
            queryset = (
                queryset.filter(
                    featured=False
                )
            )

        return queryset