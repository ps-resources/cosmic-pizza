"""Tests for the Order model."""

import pytest

from pizzeria.orders import Order


def test_add_topping_builds_receipt():
    order = Order("large")
    order.add_topping("pepperoni").add_topping("olives")
    receipt = order.receipt()
    assert receipt["size"] == "large"
    assert receipt["toppings"] == ["pepperoni", "olives"]
    # large base 1499 + pepperoni 150 + olives 100 = 1749
    assert receipt["price"] == "$17.49"


def test_remove_topping():
    order = Order("medium")
    order.add_topping("bacon").add_topping("basil")
    order.remove_topping("bacon")
    assert order.toppings == ["basil"]


def test_add_unknown_topping_raises():
    order = Order("small")
    with pytest.raises(ValueError):
        order.add_topping("moon rocks")
