"""
Serializers for the Cinematic SGnG Marketplace catalog API.

This module converts Category and Product model instances into API-friendly representations and validates incoming catalog data.

The public API is currently configured as read-only, but keeping serializer validation in place provides a strong foundation for future staff-authorized API create/update functionality.
"""

from decimal import Decimal

from rest_framework import serializers

from .models import Category, Product


# =========================================================
# CATEGORY SERIALIZER
# =========================================================


class CategorySerializer(serializers.ModelSerializer):
    """
    Serialize SGnG marketplace categories.

    The serializer exposes identifying information, descriptive information, availability state, and the number of active products currently assigned to each category.
    """

    product_count = serializers.SerializerMethodField()

    category_url = serializers.SerializerMethodField()

    class Meta:
        model = Category

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "active",
            "product_count",
            "category_url",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "slug",
            "product_count",
            "category_url",
            "created_at",
            "updated_at",
        )


    # -----------------------------------------------------
    # CATEGORY PRODUCT COUNT
    # -----------------------------------------------------

    def get_product_count(self, obj):
        """
        Return the number of active products currently associated with the category.

        Only active products are included because inactive marketplace products are not exposed through the customer-facing catalog.
        """

        return obj.products.filter(
            active=True,
        ).count()


    # -----------------------------------------------------
    # CATEGORY API URL
    # -----------------------------------------------------

    def get_category_url(self, obj):
        """
        Return an API URL for the category when request context is available.

        The category API uses the category slug as its lookup value.
        """

        request = self.context.get("request")

        relative_url = (
            f"/api/catalog/categories/{obj.slug}/"
        )

        if request is not None:
            return request.build_absolute_uri(
                relative_url
            )

        return relative_url


    # -----------------------------------------------------
    # CATEGORY NAME VALIDATION
    # -----------------------------------------------------

    def validate_name(self, value):
        """
        Normalize and validate the category name.

        Category names may not contain only whitespace.
        """

        cleaned_value = value.strip()

        if not cleaned_value:
            raise serializers.ValidationError(
                "Category name cannot be empty."
            )

        return cleaned_value


    # -----------------------------------------------------
    # CATEGORY DESCRIPTION VALIDATION
    # -----------------------------------------------------

    def validate_description(self, value):
        """
        Normalize optional category descriptions.
        """

        if value is None:
            return ""

        return value.strip()


# =========================================================
# PRODUCT SERIALIZER
# =========================================================


class ProductSerializer(serializers.ModelSerializer):
    """
    Serialize products within the Cinematic SGnG Marketplace.

    In addition to fields stored directly on the Product model, the serializer exposes several calculated and human-readable properties:

    - Category name
    - Category slug
    - Human-readable condition
    - Savings amount
    - Savings percentage
    - Product availability
    - Product Detail URL
    - Product image URL
    """


    # =====================================================
    # CATEGORY REPRESENTATION
    # =====================================================

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    category_slug = serializers.CharField(
        source="category.slug",
        read_only=True,
    )


    # =====================================================
    # CONDITION REPRESENTATION
    # =====================================================

    condition_display = (
        serializers.SerializerMethodField()
    )


    # =====================================================
    # CALCULATED MARKETPLACE VALUES
    # =====================================================

    savings_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    savings_percentage = serializers.IntegerField(
        read_only=True,
    )

    is_available = serializers.BooleanField(
        read_only=True,
    )


    # =====================================================
    # URL REPRESENTATION
    # =====================================================

    product_url = serializers.SerializerMethodField()

    api_url = serializers.SerializerMethodField()

    image_url = serializers.SerializerMethodField()


    # =====================================================
    # META
    # =====================================================

    class Meta:
        model = Product

        fields = (
            "id",

            # Category
            "category",
            "category_name",
            "category_slug",

            # Product Identity
            "name",
            "slug",
            "description",

            # Condition
            "condition",
            "condition_display",

            # Pricing
            "sgng_price",
            "reference_price",
            "savings_amount",
            "savings_percentage",

            # External Reference
            "external_reference_url",

            # Product Media
            "image",
            "image_url",

            # Inventory
            "inventory_quantity",
            "is_available",

            # Marketplace Display
            "featured",
            "active",

            # URLs
            "product_url",
            "api_url",

            # Record Information
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "slug",

            "category_name",
            "category_slug",

            "condition_display",

            "savings_amount",
            "savings_percentage",
            "is_available",

            "product_url",
            "api_url",
            "image_url",

            "created_at",
            "updated_at",
        )


    # =====================================================
    # CONDITION DISPLAY
    # =====================================================

    def get_condition_display(self, obj):
        """
        Return the human-readable condition label.

        Examples:

        "new"          -> "New"
        "gently_used" -> "Gently Used"
        """

        return obj.get_condition_display()


    # =====================================================
    # PRODUCT DETAIL URL
    # =====================================================

    def get_product_url(self, obj):
        """
        Return the customer-facing HTML Product Detail URL.

        When request context is available, return an absolute URL.

        Otherwise, return the relative Django URL.
        """

        relative_url = obj.get_absolute_url()

        request = self.context.get("request")

        if request is not None:
            return request.build_absolute_uri(
                relative_url
            )

        return relative_url


    # =====================================================
    # API DETAIL URL
    # =====================================================

    def get_api_url(self, obj):
        """
        Return the product's API detail endpoint.

        The Product API uses the product slug as the lookup value.
        """

        relative_url = (
            f"/api/catalog/products/{obj.slug}/"
        )

        request = self.context.get("request")

        if request is not None:
            return request.build_absolute_uri(
                relative_url
            )

        return relative_url


    # =====================================================
    # PRODUCT IMAGE URL
    # =====================================================

    def get_image_url(self, obj):
        """
        Return an absolute product-image URL when an image exists.

        Return None when no image has been uploaded.
        """

        if not obj.image:
            return None

        image_url = obj.image.url

        request = self.context.get("request")

        if request is not None:
            return request.build_absolute_uri(
                image_url
            )

        return image_url


    # =====================================================
    # PRODUCT NAME VALIDATION
    # =====================================================

    def validate_name(self, value):
        """
        Normalize and validate the Product name.

        Product names may not contain only whitespace.
        """

        cleaned_value = value.strip()

        if not cleaned_value:
            raise serializers.ValidationError(
                "Product name cannot be empty."
            )

        return cleaned_value


    # =====================================================
    # PRODUCT DESCRIPTION VALIDATION
    # =====================================================

    def validate_description(self, value):
        """
        Normalize and validate the Product description.

        Every marketplace Product must contain meaningful
        descriptive content.
        """

        cleaned_value = value.strip()

        if not cleaned_value:
            raise serializers.ValidationError(
                "Product description cannot be empty."
            )

        return cleaned_value


    # =====================================================
    # CONDITION VALIDATION
    # =====================================================

    def validate_condition(self, value):
        """
        Ensure the submitted condition matches one of the
        condition values defined by the Product model.
        """

        valid_conditions = {
            condition_value
            for condition_value, condition_label
            in Product.Condition.choices
        }

        if value not in valid_conditions:
            raise serializers.ValidationError(
                "Select a valid product condition."
            )

        return value


    # =====================================================
    # SGnG PRICE VALIDATION
    # =====================================================

    def validate_sgng_price(self, value):
        """
        Prevent negative SGnG prices.
        """

        if value < Decimal("0.00"):
            raise serializers.ValidationError(
                "SGnG price cannot be negative."
            )

        return value


    # =====================================================
    # REFERENCE PRICE VALIDATION
    # =====================================================

    def validate_reference_price(
        self,
        value,
    ):
        """
        Permit an empty reference price while preventing
        negative reference prices.
        """

        if (
            value is not None
            and value < Decimal("0.00")
        ):
            raise serializers.ValidationError(
                "Reference price cannot be negative."
            )

        return value


    # =====================================================
    # INVENTORY VALIDATION
    # =====================================================

    def validate_inventory_quantity(
        self,
        value,
    ):
        """
        Prevent negative inventory quantities.

        Product.inventory_quantity uses a positive integer
        model field, but this explicit serializer rule keeps
        the API behavior clear and self-documenting.
        """

        if value < 0:
            raise serializers.ValidationError(
                (
                    "Inventory quantity cannot "
                    "be negative."
                )
            )

        return value


    # =====================================================
    # EXTERNAL REFERENCE URL VALIDATION
    # =====================================================

    def validate_external_reference_url(
        self,
        value,
    ):
        """
        Permit an empty external reference URL.

        When supplied, URL syntax is also handled by the
        serializer/model URL field.
        """

        if not value:
            return ""

        return value.strip()


    # =====================================================
    # OBJECT-LEVEL PRODUCT VALIDATION
    # =====================================================

    def validate(self, attrs):
        """
        Perform validation involving more than one Product
        field.

        A reference price is optional. When supplied, SGnG
        permits it to equal or exceed the SGnG selling
        price.

        If the reference price is lower than the SGnG price,
        the record is rejected because presenting that value
        as a reference price would make the marketplace
        savings calculation inappropriate.
        """

        instance = getattr(
            self,
            "instance",
            None,
        )

        sgng_price = attrs.get(
            "sgng_price",
            getattr(
                instance,
                "sgng_price",
                None,
            ),
        )

        reference_price = attrs.get(
            "reference_price",
            getattr(
                instance,
                "reference_price",
                None,
            ),
        )

        if (
            reference_price is not None
            and sgng_price is not None
            and reference_price < sgng_price
        ):
            raise serializers.ValidationError(
                {
                    "reference_price": (
                        "Reference price cannot be "
                        "lower than the SGnG price."
                    )
                }
            )

        return attrs