from django.urls import path

from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductManagementView,
    ProductUpdateView,
)


app_name = "catalog"


urlpatterns = [
    # =====================================================
    # PUBLIC MARKETPLACE
    # =====================================================

    path(
        "",
        ProductListView.as_view(),
        name="product-list",
    ),

    # =====================================================
    # STAFF PRODUCT MANAGEMENT
    # =====================================================

    path(
        "staff/products/",
        ProductManagementView.as_view(),
        name="product-management",
    ),

    path(
        "staff/products/create/",
        ProductCreateView.as_view(),
        name="product-create",
    ),

    path(
        "staff/products/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product-update",
    ),

    path(
        "staff/products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product-delete",
    ),

    # =====================================================
    # PRODUCT DETAIL

    # Keep this LAST so "staff/..." routes are resolved
    # before Django treats "staff" as a product slug.
    # =====================================================

    path(
        "<slug:slug>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
]