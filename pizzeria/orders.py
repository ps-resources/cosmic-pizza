"""Order modeling for Cosmic Pizza."""

from pizzeria.menu import TOPPINGS
from pizzeria.pricing import calculate_calories, calculate_price, format_price


class Order:
    """A single pizza order: one size plus a list of toppings."""

    def __init__(self, size):
        self.size = size
        self.toppings = []

    def add_topping(self, name):
        """Add a topping to the order if it exists on the menu."""
        if name not in TOPPINGS:
            raise ValueError(f"Unknown topping: {name}")
        self.toppings.append(name)
        return self

    def remove_topping(self, name):
        """Remove a topping from the order if present."""
        if name in self.toppings:
            self.toppings.remove(name)
        return self

    def price(self):
        """Total price in cents."""
        return calculate_price(self.size, self.toppings)

    def calories(self):
        """Total calories."""
        return calculate_calories(self.size, self.toppings)

    def receipt(self):
        """Return a human-readable receipt as a dictionary."""
        return {
            "size": self.size,
            "toppings": list(self.toppings),
            "price": format_price(self.price()),
            "calories": self.calories(),
        }
