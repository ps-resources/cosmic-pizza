"""Tests for pricing calculations.

These intentionally do NOT cover every function (for example, calorie totals
and JSON menu formatting are left untested) so the demo can show a code coverage
gap on the first scan.
"""

import pytest

from pizzeria.pricing import calculate_price, find_topping, format_price


def test_base_price_no_toppings():
    assert calculate_price("small", []) == 899


def test_price_with_toppings():
    # medium base 1199 + pepperoni 150 + mushroom 100
    assert calculate_price("medium", ["pepperoni", "mushroom"]) == 1449


def test_unknown_topping_is_ignored():
    assert calculate_price("small", ["moon rocks"]) == 899


def test_unknown_size_raises():
    with pytest.raises(ValueError):
        calculate_price("jumbo", [])


def test_find_topping_returns_details():
    details = find_topping("bacon")
    assert details["category"] == "meat"


def test_find_unknown_topping_returns_none():
    assert find_topping("moon rocks") is None


def test_format_price():
    assert format_price(1299) == "$12.99"
