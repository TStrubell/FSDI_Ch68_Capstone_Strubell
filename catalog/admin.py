from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "condition",
        "sgng_price",
        "reference_price",
        "inventory_quantity",
        "featured",
        "active",
        "updated_at",
    )

    list_filter = (
        "active",
        "featured",
        "condition",
        "category",
    )

    search_fields = (
        "name",
        "description",
        "category__name",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_editable = (
        "inventory_quantity",
        "featured",
        "active",
    )

    ordering = (
        "-featured",
        "-created_at",
    )

    fieldsets = (
        (
            "Product Information",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "description",
                    "condition",
                    "image",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "sgng_price",
                    "reference_price",
                    "external_reference_url",
                )
            },
        ),
        (
            "Inventory and Display",
            {
                "fields": (
                    "inventory_quantity",
                    "featured",
                    "active",
                )
            },
        ),
        (
            "Record Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    