from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Product


PRODUCT_IMAGES = {
    "Adventure Carabiner Key Clip": (
        "adventure_carabiner_key_clip.jpg"
    ),
    "Alpine Ridge Daypack": (
        "alpine_ridge_daypack.jpg"
    ),
    "Basecamp Logo Cap": (
        "basecamp_logo_cap.jpg"
    ),
    "Cedar Trail Camp Blanket": (
        "cedar_trail_camp_blanket.jpg"
    ),
    "Compact Trail Multi-Tool": (
        "compact_trail_multi_tool.jpg"
    ),
    "Field Repair Tool Roll": (
        "field_repair_tool_roll.jpg"
    ),
    "Frontier Leather Field Journal": (
        "frontier_leather_field_journal.jpg"
    ),
    "Heritage Leather Card Wallet": (
        "heritage_leather_card_wallet.jpg"
    ),
    "Highland Trekking Pole Set": (
        "highland_trekking_pole_set.jpg"
    ),
    "Navigator Compass Keychain": (
        "navigator_compass_keychain.jpg"
    ),
    "Ridgeline Utility Hoodie": (
        "ridgeline_utility_hoodie.jpg"
    ),
    "Ridgeway Leather Utility Pouch": (
        "ridgeway_leather_utility_pouch.jpg"
    ),
    "Summit Camp Lantern": (
        "summit_camp_lantern.jpg"
    ),
    "Trailhead Folding Shovel": (
        "trailhead_folding_shovel.jpg"
    ),
}


class Command(BaseCommand):
    help = (
        "Attach the 14 Assignment 2 source images "
        "to their corresponding SGnG Products."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help=(
                "Replace an existing Product image "
                "with the mapped Assignment 2 image."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        source_directory = (
            Path(settings.BASE_DIR)
            / "catalog"
            / "seed_assets"
            / "product_images"
        )

        replace_images = options["replace"]

        if not source_directory.exists():
            self.stderr.write(
                self.style.ERROR(
                    (
                        "The source-image directory does not exist: "
                        f"{source_directory}"
                    )
                )
            )
            return

        missing_source_files = []
        missing_products = []

        for product_name, filename in PRODUCT_IMAGES.items():
            source_path = (
                source_directory
                / filename
            )

            if not source_path.is_file():
                missing_source_files.append(
                    str(source_path)
                )

            if not Product.objects.filter(
                name=product_name
            ).exists():
                missing_products.append(
                    product_name
                )

        if missing_source_files:
            self.stderr.write(
                self.style.ERROR(
                    "Missing source-image files:"
                )
            )

            for source_file in missing_source_files:
                self.stderr.write(
                    f"  - {source_file}"
                )

        if missing_products:
            self.stderr.write(
                self.style.ERROR(
                    "Missing Product records:"
                )
            )

            for product_name in missing_products:
                self.stderr.write(
                    f"  - {product_name}"
                )

        if (
            missing_source_files
            or missing_products
        ):
            self.stderr.write(
                self.style.ERROR(
                    (
                        "No Product images were changed. "
                        "Correct every missing file or Product "
                        "and run the command again."
                    )
                )
            )
            return

        attached_count = 0
        skipped_count = 0

        for product_name, filename in PRODUCT_IMAGES.items():
            product = Product.objects.get(
                name=product_name
            )

            source_path = (
                source_directory
                / filename
            )

            if (
                product.image
                and not replace_images
            ):
                skipped_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        (
                            "Skipped existing image: "
                            f"{product.name} -> "
                            f"{product.image.name}"
                        )
                    )
                )

                continue

            if (
                product.image
                and replace_images
            ):
                product.image.delete(
                    save=False
                )

            with source_path.open("rb") as image_file:
                product.image.save(
                    filename,
                    File(image_file),
                    save=False,
                )

            product.save(
                update_fields=[
                    "image",
                    "updated_at",
                ]
            )

            attached_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    (
                        "Attached image: "
                        f"{product.name} -> "
                        f"{product.image.name}"
                    )
                )
            )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Assignment 2 Product-image integration "
                    "completed. "
                    f"Attached: {attached_count}; "
                    f"Skipped: {skipped_count}."
                )
            )
        )