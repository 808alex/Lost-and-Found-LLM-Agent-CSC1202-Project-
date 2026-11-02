from django.conf import settings
from django.db import models


class Item(models.Model):
    # Fixed lists so search filters work, and so the LLM agent has to pick
    # one of these instead of inventing its own wording.
    class Category(models.TextChoices):
        PHONE = "phone", "Phone"
        WALLET = "wallet", "Wallet / purse"
        KEYS = "keys", "Keys"
        BAG = "bag", "Bag / backpack"
        LAPTOP = "laptop", "Laptop / tablet"
        HEADPHONES = "headphones", "Headphones / earbuds"
        CLOTHING = "clothing", "Clothing"
        BOTTLE = "bottle", "Water bottle"
        CARD = "card", "ID / student card"
        JEWELLERY = "jewellery", "Jewellery / watch"
        OTHER = "other", "Other"

    class Colour(models.TextChoices):
        BLACK = "black", "Black"
        WHITE = "white", "White"
        GREY = "grey", "Grey"
        SILVER = "silver", "Silver"
        GOLD = "gold", "Gold"
        RED = "red", "Red"
        ORANGE = "orange", "Orange"
        YELLOW = "yellow", "Yellow"
        GREEN = "green", "Green"
        BLUE = "blue", "Blue"
        PURPLE = "purple", "Purple"
        PINK = "pink", "Pink"
        BROWN = "brown", "Brown"
        MULTI = "multi", "Multicoloured"

    class Kind(models.TextChoices):
        LOST = "lost", "Lost"
        FOUND = "found", "Found"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        MATCHED = "matched", "Matched"
        RETURNED = "returned", "Returned"

    kind = models.CharField(max_length=5, choices=Kind.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    # What the user typed
    description = models.TextField()
    photo = models.ImageField(upload_to="items/", blank=True)
    date = models.DateField(help_text="When it was lost/found")

    # Filled in by the LLM agent from the description/photo
    object_type = models.CharField(max_length=100, choices=Category.choices, blank=True)
    colour = models.CharField(max_length=50, choices=Colour.choices, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    features = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_kind_display()}: {self.get_object_type_display() or self.description[:40]}"
