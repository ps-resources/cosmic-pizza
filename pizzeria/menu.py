"""Cosmic Pizza menu data: sizes and toppings.

This is the single source of truth for what the pizzeria sells. Prices are in
whole US cents to avoid floating point rounding surprises.
"""

# size name -> (base price in cents, base calories)
SIZES = {
    "small": (899, 600),
    "medium": (1199, 900),
    "large": (1499, 1300),
    "galactic": (1999, 1800),
}

# Each topping: name -> {price (cents), calories, category}
TOPPINGS = {
    "pepperoni": {"price": 150, "calories": 120, "category": "meat"},
    "mushroom": {"price": 100, "calories": 30, "category": "veggie"},
    "extra cheese": {"price": 200, "calories": 180, "category": "dairy"},
    "olives": {"price": 100, "calories": 50, "category": "veggie"},
    "pineapple": {"price": 125, "calories": 80, "category": "fruit"},
    "jalapeno": {"price": 75, "calories": 10, "category": "veggie"},
    "bacon": {"price": 175, "calories": 140, "category": "meat"},
    "basil": {"price": 50, "calories": 5, "category": "veggie"},
    "anchovy": {"price": 160, "calories": 60, "category": "meat"},
    "stardust": {"price": 300, "calories": 0, "category": "cosmic"},
}

# Display labels for the storefront category filter. "veggie" is listed twice ->
# CodeQL "Duplicate key in dict literal" reliability finding; the later value
# silently wins, so the first "Garden" label is dead.
CATEGORY_LABELS = {
    "meat": "Meaty",
    "veggie": "Garden",
    "dairy": "Dairy",
    "fruit": "Fruity",
    "veggie": "Veggie",
    "cosmic": "Cosmic",
}


def size_names():
    """Return the list of available size names."""
    return list(SIZES.keys())


def topping_names():
    """Return the list of available topping names."""
    return list(TOPPINGS.keys())
