from decimal import Decimal

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
        return self.active and self.inventory_quantity > 0

    @property
    def savings_amount(self):
        if (
            self.reference_price is not None
            and self.reference_price > self.sgng_price
        ):
            return self.reference_price - self.sgng_price

        return Decimal("0.00")

    @property
    def savings_percentage(self):
        if (
            self.reference_price is not None
            and self.reference_price > 0
            and self.reference_price > self.sgng_price
        ):
            percentage = (
                self.savings_amount / self.reference_price
            ) * Decimal("100")

            return percentage.quantize(Decimal("0.01"))

        return Decimal("0.00")