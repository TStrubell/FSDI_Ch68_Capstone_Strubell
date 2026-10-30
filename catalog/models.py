from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def emoji(self):
        emoji_map = {
            "outdoor-gear": "⛺",
            "leather-goods": "🧰",
            "tools": "🔧",
            "accessories": "🎒",
            "apparel": "👕",
        }

        return emoji_map.get(
            self.slug,
            "🏷️",
        )


    @property
    def display_name(self):
        return f"{self.emoji} {self.name}"
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Product(models.Model):
    class Condition(models.TextChoices):
        NEW = "new", "New"
        GENTLY_USED = "gently_used", "Gently Used"

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    name = models.CharField(
        max_length=150,
    )

    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
    )

    description = models.TextField()

    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.NEW,
    )

    sgng_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    reference_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        blank=True,
        null=True,
    )

    external_reference_url = models.URLField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )

    inventory_quantity = models.PositiveIntegerField(
        default=0,
    )

    featured = models.BooleanField(
        default=False,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-featured", "-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            candidate_slug = base_slug
            counter = 2

            while Product.objects.exclude(pk=self.pk).filter(
                slug=candidate_slug
            ).exists():
                candidate_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = candidate_slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "catalog:product-detail",
            kwargs={"slug": self.slug},
        )

    @property
    def is_available(self):
        return (
            self.active 
            and self.inventory_quantity > 0
        )

    @property
    def savings_amount(self):
        """
        Return the difference between the reference price and the SGnG price.

        Returns zero when no valid reference-price savings exist.

        Example:
            Reference Price: $39.99
            SGnG Price:      $29.99
            Savings:         $10.00
        """

        if (
            self.reference_price is not None
            and self.reference_price > self.sgng_price
        ):
            return (
                self.reference_price
                - self.sgng_price
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

        return Decimal("0.00")

    @property
    def savings_percentage(self):
        """
        Return the customer's savings as a percentage of the reference price, rounded to two decimal places.

        Examples:
            25.01% -> 25%
            25.49% -> 25%
            25.50% -> 26%
            37.50% -> 38%
        """

        if (
            self.reference_price is not None
            and self.reference_price > 0
            and self.reference_price > self.sgng_price
        ):
            percentage = (
                self.savings_amount
                / self.reference_price
            ) * Decimal("100")

            return percentage.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
            )

        return Decimal("0.00")