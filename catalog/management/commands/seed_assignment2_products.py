from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Category, Product


CATEGORY_DATA = {
    "Outdoor Gear": {
        "description": (
            "Trail, campsite, and outdoor-use equipment."
        ),
        "active": True,
    },
    "Leather Goods": {
        "description": (
            "Practical leather accessories and carry goods."
        ),
        "active": True,
    },
    "Tools": {
        "description": (
            "Compact tools for outdoor and everyday use."
        ),
        "active": True,
    },
    "Accessories": {
        "description": (
            "Useful accessories for travel and daily carry."
        ),
        "active": True,
    },
    "Apparel": {
        "description": (
            "Outdoor-inspired clothing and wearable gear."
        ),
        "active": True,
    },
}


PRODUCT_DATA = [
    {
        "category": "Outdoor Gear",
        "name": "Alpine Ridge Daypack",
        "description": (
            "A compact daypack with organized storage "
            "for short hikes, day trips, and everyday travel."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("44.99"),
        "reference_price": Decimal("64.99"),
        "inventory_quantity": 7,
        "featured": True,
        "active": True,
    },
    {
        "category": "Outdoor Gear",
        "name": "Cedar Trail Camp Blanket",
        "description": (
            "A durable camp blanket designed for cool evenings, "
            "picnic stops, and organized vehicle storage."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("39.99"),
        "reference_price": Decimal("59.99"),
        "inventory_quantity": 5,
        "featured": False,
        "active": True,
    },
    {
        "category": "Outdoor Gear",
        "name": "Highland Trekking Pole Set",
        "description": (
            "An adjustable trekking-pole pair for supported "
            "walking on established trails and varied terrain."
        ),
        "condition": Product.Condition.GENTLY_USED,
        "sgng_price": Decimal("34.99"),
        "reference_price": Decimal("54.99"),
        "inventory_quantity": 3,
        "featured": False,
        "active": True,
    },
    {
        "category": "Outdoor Gear",
        "name": "Summit Camp Lantern",
        "description": (
            "A portable lantern for campsite tables, tents, "
            "emergency kits, and evening outdoor activities."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("29.99"),
        "reference_price": Decimal("44.99"),
        "inventory_quantity": 8,
        "featured": True,
        "active": True,
    },
    {
        "category": "Leather Goods",
        "name": "Frontier Leather Field Journal",
        "description": (
            "A refillable leather journal cover for trail notes, "
            "planning pages, and everyday written records."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("32.99"),
        "reference_price": Decimal("49.99"),
        "inventory_quantity": 6,
        "featured": True,
        "active": True,
    },
    {
        "category": "Leather Goods",
        "name": "Heritage Leather Card Wallet",
        "description": (
            "A slim leather card wallet with a compact profile "
            "for frequently used cards and folded currency."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("24.99"),
        "reference_price": Decimal("34.99"),
        "inventory_quantity": 10,
        "featured": False,
        "active": True,
    },
    {
        "category": "Leather Goods",
        "name": "Ridgeway Leather Utility Pouch",
        "description": (
            "A zippered leather utility pouch for cables, "
            "small tools, field supplies, or travel essentials."
        ),
        "condition": Product.Condition.GENTLY_USED,
        "sgng_price": Decimal("27.99"),
        "reference_price": Decimal("42.99"),
        "inventory_quantity": 4,
        "featured": False,
        "active": True,
    },
    {
        "category": "Tools",
        "name": "Compact Trail Multi-Tool",
        "description": (
            "A compact multi-tool for routine adjustments, "
            "light campsite tasks, and organized gear kits."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("21.99"),
        "reference_price": Decimal("31.99"),
        "inventory_quantity": 9,
        "featured": True,
        "active": True,
    },
    {
        "category": "Tools",
        "name": "Field Repair Tool Roll",
        "description": (
            "A roll-style organizer for compact hand tools, "
            "repair accessories, and frequently used supplies."
        ),
        "condition": Product.Condition.GENTLY_USED,
        "sgng_price": Decimal("26.99"),
        "reference_price": Decimal("39.99"),
        "inventory_quantity": 2,
        "featured": False,
        "active": True,
    },
    {
        "category": "Tools",
        "name": "Trailhead Folding Shovel",
        "description": (
            "A folding utility shovel intended for campsite "
            "maintenance, vehicle kits, and outdoor preparation."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("36.99"),
        "reference_price": Decimal("52.99"),
        "inventory_quantity": 5,
        "featured": False,
        "active": True,
    },
    {
        "category": "Accessories",
        "name": "Adventure Carabiner Key Clip",
        "description": (
            "A lightweight accessory clip for keys and small "
            "everyday-carry items. Not intended for climbing."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("9.99"),
        "reference_price": Decimal("14.99"),
        "inventory_quantity": 15,
        "featured": False,
        "active": True,
    },
    {
        "category": "Accessories",
        "name": "Insulated Trail Bottle",
        "description": (
            "A reusable insulated bottle for carrying cold "
            "or warm beverages during travel and outdoor use."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("19.99"),
        "reference_price": Decimal("29.99"),
        "inventory_quantity": 12,
        "featured": True,
        "active": True,
    },
    {
        "category": "Accessories",
        "name": "Navigator Compass Keychain",
        "description": (
            "A compact compass-themed keychain accessory "
            "for packs, keys, and outdoor-inspired collections."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("12.99"),
        "reference_price": Decimal("18.99"),
        "inventory_quantity": 11,
        "featured": False,
        "active": True,
    },
    {
        "category": "Apparel",
        "name": "Basecamp Logo Cap",
        "description": (
            "An adjustable cap with SGnG-inspired styling "
            "for casual outdoor and everyday wear."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("22.99"),
        "reference_price": Decimal("32.99"),
        "inventory_quantity": 8,
        "featured": False,
        "active": True,
    },
    {
        "category": "Apparel",
        "name": "Ridgeline Utility Hoodie",
        "description": (
            "A comfortable utility hoodie designed for layering "
            "during cool-weather travel and casual outdoor use."
        ),
        "condition": Product.Condition.NEW,
        "sgng_price": Decimal("49.99"),
        "reference_price": Decimal("69.99"),
        "inventory_quantity": 6,
        "featured": True,
        "active": True,
    },
]


class Command(BaseCommand):
    help = (
        "Create or update the controlled 15-Product "
        "FSDI-120 Assignment 2 demonstration dataset."
    )

    def handle(self, *args, **options):
        categories = {}

        for name, defaults in CATEGORY_DATA.items():
            category, created = Category.objects.update_or_create(
                name=name,
                defaults=defaults,
            )

            categories[name] = category

            action = "Created" if created else "Updated"

            self.stdout.write(
                f"{action} Category: {name}"
            )

        created_count = 0
        updated_count = 0

        for item in PRODUCT_DATA:
            category_name = item["category"]

            defaults = {
                key: value
                for key, value in item.items()
                if key not in {"category", "name"}
            }

            defaults["category"] = categories[category_name]

            product, created = Product.objects.update_or_create(
                name=item["name"],
                defaults=defaults,
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

            self.stdout.write(
                (
                    f"{'Created' if created else 'Updated'} "
                    f"Product: {product.name}"
                )
            )

        public_count = Product.objects.filter(
            active=True,
            category__active=True,
        ).count()

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Assignment 2 seed complete. "
                    f"Created: {created_count}; "
                    f"Updated: {updated_count}; "
                    f"Public active Products: {public_count}."
                )
            )
        )