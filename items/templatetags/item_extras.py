from django import template

register = template.Library()

CATEGORY_ICONS = {
    "phone": "📱",
    "wallet": "👛",
    "keys": "🔑",
    "bag": "🎒",
    "laptop": "💻",
    "headphones": "🎧",
    "clothing": "🧥",
    "bottle": "🧴",
    "card": "🪪",
    "jewellery": "⌚",
    "other": "📦",
}


@register.filter
def category_icon(object_type):
    """Emoji shown in place of a photo for an item's category."""
    return CATEGORY_ICONS.get(object_type, "📦")
