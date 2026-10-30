from decimal import Decimal

from django import forms

from .models import Category, Product


class ProductForm(forms.ModelForm):
    """
    Staff form used to create and update SGnG products.
    """

    class Meta:
        model = Product

        fields = (
            "category",
            "name",
            "description",
            "condition",
            "sgng_price",
            "reference_price",
            "external_reference_url",
            "image",
            "inventory_quantity",
            "featured",
            "active",
        )

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product name",
                    "autocomplete": "off",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 7,
                    "placeholder": (
                        "Describe the product, its intended use, "
                        "condition, and relevant characteristics."
                    ),
                }
            ),
            "condition": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "sgng_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "0.00",
                }
            ),
            "reference_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "Optional",
                }
            ),
            "external_reference_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "https://example.com/reference-product"
                    ),
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "inventory_quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "1",
                }
            ),
            "featured": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
        }

        help_texts = {
            "category": (
                "Select the marketplace category for this product."
            ),
            "name": (
                "Enter a clear, customer-facing product name."
            ),
            "description": (
                "Describe the product without making unsupported "
                "performance, safety, or certification claims."
            ),
            "sgng_price": (
                "Enter the current SGnG marketplace price."
            ),
            "reference_price": (
                "Optional comparison price used to calculate savings."
            ),
            "external_reference_url": (
                "Optional URL to a legitimate external reference page."
            ),
            "image": (
                "Upload a representative product image."
            ),
            "inventory_quantity": (
                "Enter zero when the product is unavailable."
            ),
            "featured": (
                "Featured products may appear on the Homepage."
            ),
            "active": (
                "Inactive products are hidden from the public Marketplace."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = (
            Category.objects
            .filter(active=True)
            .order_by("name")
        )

        self.fields["reference_price"].required = False
        self.fields["external_reference_url"].required = False
        self.fields["image"].required = False

    def clean_sgng_price(self):
        sgng_price = self.cleaned_data.get(
            "sgng_price"
        )

        if (
            sgng_price is not None
            and sgng_price < Decimal("0.00")
        ):
            raise forms.ValidationError(
                "SGnG price cannot be negative."
            )

        return sgng_price

    def clean_reference_price(self):
        reference_price = self.cleaned_data.get(
            "reference_price"
        )

        if (
            reference_price is not None
            and reference_price < Decimal("0.00")
        ):
            raise forms.ValidationError(
                "Reference price cannot be negative."
            )

        return reference_price

    def clean_inventory_quantity(self):
        inventory_quantity = self.cleaned_data.get(
            "inventory_quantity"
        )

        if (
            inventory_quantity is not None
            and inventory_quantity < 0
        ):
            raise forms.ValidationError(
                "Inventory quantity cannot be negative."
            )

        return inventory_quantity

    def clean(self):
        cleaned_data = super().clean()

        sgng_price = cleaned_data.get(
            "sgng_price"
        )

        reference_price = cleaned_data.get(
            "reference_price"
        )

        if (
            sgng_price is not None
            and reference_price is not None
            and reference_price < sgng_price
        ):
            self.add_error(
                "reference_price",
                (
                    "Reference price must be greater than or "
                    "equal to the SGnG price."
                ),
            )

        return cleaned_data