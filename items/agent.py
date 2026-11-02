"""
The LLM agent's two jobs. Both are PLACEHOLDERS for now: they use simple
keyword matching so the site works before the LLM is plugged in.

When the team picks an LLM API, replace the body of each function with an
LLM call. The views don't need to change, because the inputs and outputs
stay the same.
"""
import re

from .models import Item

# Placeholder only: the LLM will understand descriptions without a word list.
CATEGORY_KEYWORDS = {
    "phone": {"phone", "iphone", "samsung", "mobile"},
    "wallet": {"wallet", "purse"},
    "keys": {"key", "keys", "keyring"},
    "bag": {"bag", "backpack", "rucksack", "handbag", "tote"},
    "laptop": {"laptop", "macbook", "tablet", "ipad", "chromebook"},
    "headphones": {"headphones", "earbuds", "airpods", "earphones"},
    "clothing": {"jacket", "coat", "hoodie", "jumper", "scarf", "hat", "gloves"},
    "bottle": {"bottle", "flask"},
    "card": {"leapcard", "idcard", "studentcard"},
    "jewellery": {"ring", "necklace", "bracelet", "watch", "earring", "earrings"},
}


def extract_attributes(description):
    """
    Job 1: on Report, turn a free-text description into structured fields.

    LLM version: send the description (and photo) to the LLM and ask for JSON
    like {"object_type": "bag", "colour": "black", "brand": "Nike"}, where
    object_type and colour must come from Item.Category / Item.Colour.
    """
    words = set(_words(description))
    attributes = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        if words & keywords:
            attributes["object_type"] = category
            break
    for value, _ in Item.Colour.choices:
        if value in words:
            attributes["colour"] = value
            break
    return attributes


def find_matches(query, items):
    """
    Job 2: on Find, rank found items by how well they match what the person
    typed, e.g. "black nike backpack I left in the library".

    LLM version: give the LLM the query plus each candidate item's
    description and attributes, and ask it to return the best matches with
    a score and a short reason ("same colour and brand, found nearby").
    """
    query_words = set(_words(query)) - STOPWORDS
    if not query_words:
        return list(items)

    scored = []
    for item in items:
        text = " ".join([
            item.description, item.object_type, item.colour, item.brand, item.location,
            item.get_object_type_display(),
        ])
        score = len(query_words & set(_words(text)))
        if score:
            scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored]


STOPWORDS = {"a", "an", "the", "i", "my", "it", "in", "on", "at", "of", "with", "and", "lost", "left", "near"}


def _words(text):
    return re.findall(r"[a-z]+", text.lower())
