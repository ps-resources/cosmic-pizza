"""Pricing and nutrition calculations for Cosmic Pizza.

NOTE: This module intentionally contains a few mild code-quality issues so that
the very first Code Quality scan surfaces something to review and fix during the
demo. Keep them subtle; the big, obvious demo findings are injected later by the
"Introduce code quality issues" Actions workflow.
"""

import json  # unused import -> CodeQL "Unused import" quality finding

from pizzeria.menu import SIZES, TOPPINGS


def find_topping(name):
    """Look up a topping by name.

    This walks the whole topping list every call instead of using a direct
    dictionary lookup. It works, but it is O(n) per call and gets slower as the
    menu grows.
    """
    for topping_name, details in TOPPINGS.items():
        if topping_name == name:
            return details
    return None


def calculate_price(size, topping_list):
    """Return the total price in cents for a pizza."""
    if size not in SIZES:
        raise ValueError(f"Unknown size: {size}")

    base_price, base_calories = SIZES[size]  # base_calories unused here
    total = base_price
    for name in topping_list:
        details = find_topping(name)
        if details is not None:
            total += details["price"]
    return total


def calculate_calories(size, topping_list):
    """Return the total calories for a pizza."""
    if size not in SIZES:
        raise ValueError(f"Unknown size: {size}")

    _, base_calories = SIZES[size]
    total = base_calories
    for name in topping_list:
        details = find_topping(name)
        if details is not None:
            total += details["calories"]
    return total


def format_price(cents):
    """Format a price in cents as a dollar string, e.g. 1299 -> '$12.99'."""
    return f"${cents / 100:.2f}"
