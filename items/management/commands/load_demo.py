"""
Fill the database with made-up found items and a demo student login, so
everyone on the team sees the same data. Safe to run more than once.

    python manage.py load_demo
"""
from datetime import date, timedelta
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from items.models import Item

DEMO_USERNAME = "student"
DEMO_PASSWORD = "dcu-demo-2026"

# (description, category, colour, brand, location, days ago)
DEMO_ITEMS = [
    ("Black Nike backpack with a keyring on the zip", "bag", "black", "Nike", "O'Reilly Library", 1),
    ("Blue iPhone 13 in a clear case, cracked corner", "phone", "blue", "Apple", "The Helix", 2),
    ("Brown leather wallet, no cards inside", "wallet", "brown", "", "U Building", 3),
    ("Set of 3 keys on a red DCU lanyard", "keys", "red", "", "Henry Grattan Building", 1),
    ("White AirPods case, no earbuds", "headphones", "white", "Apple", "Nubar", 4),
    ("Grey North Face hoodie, size M", "clothing", "grey", "The North Face", "Sports Centre", 5),
    ("Silver metal water bottle with stickers", "bottle", "silver", "Chilly's", "O'Reilly Library", 2),
    ("Silver HP laptop in a black sleeve", "laptop", "silver", "HP", "Hampstead", 6),
    ("Gold necklace with a small heart pendant", "jewellery", "gold", "", "Nursing Building", 3),
    ("Green umbrella, folding", "other", "green", "", "The Helix", 7),
]

SWATCH = {
    "black": "#222222", "white": "#f2f2f2", "grey": "#8a8f98", "silver": "#c0c4cc",
    "gold": "#d4a937", "red": "#c8102e", "orange": "#ff6600", "yellow": "#f2c811",
    "green": "#2e8b57", "blue": "#1f5fbf", "purple": "#6a3d9a", "pink": "#e88aa8",
    "brown": "#7b4a2a", "multi": "#888888",
}


def placeholder_photo(label, colour):
    """A simple square in the item's colour with its name on it."""
    background = SWATCH.get(colour, "#555555")
    image = Image.new("RGB", (400, 400), background)
    draw = ImageDraw.Draw(image)
    text_colour = "#000000" if colour in {"white", "silver", "yellow", "gold"} else "#ffffff"
    font = ImageFont.load_default(size=32)
    draw.text((200, 200), label, fill=text_colour, font=font, anchor="mm")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Load made-up found items and a demo student login."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username=DEMO_USERNAME)
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()

        added = 0
        for description, category, colour, brand, location, days_ago in DEMO_ITEMS:
            if Item.objects.filter(description=description).exists():
                continue
            item = Item(
                kind=Item.Kind.FOUND,
                description=description,
                object_type=category,
                colour=colour,
                brand=brand,
                location=location,
                date=date.today() - timedelta(days=days_ago),
            )
            label = Item.Category(category).label.split(" / ")[0]
            item.photo.save(f"demo-{category}-{colour}.png", placeholder_photo(label, colour), save=False)
            item.save()
            added += 1

        self.stdout.write(self.style.SUCCESS(f"Added {added} demo item(s)."))
        self.stdout.write(f"Demo login: {DEMO_USERNAME} / {DEMO_PASSWORD}")
