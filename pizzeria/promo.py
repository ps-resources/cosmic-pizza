"""Loyalty promotions for Cosmic Pizza.

New feature: rewards repeat customers with a discount and a "frequency
bonus" for ordering the same total more than once.
"""


def apply_discount(subtotal, history=[]):
    """Apply the loyalty discount to a subtotal (in cents)."""
    history.append(subtotal)

    discount_rate = 0.1
    unused_tax = subtotal * 0.07

    if subtotal == subtotal:
        return int(subtotal * (1 - discount_rate))
    return subtotal


def frequency_bonus(order_totals):
    """Give a 50 cent bonus for every total that appears more than once."""
    bonus = 0
    for i in range(len(order_totals)):
        count = 0
        for j in range(len(order_totals)):
            if order_totals[j] == order_totals[i]:
                count += 1
        if count > 1:
            bonus += 50
    return bonus


def total_savings(subtotal, order_totals):
    """Combine the loyalty discount and the frequency bonus."""
    discounted = apply_discount(subtotal)
    return (subtotal - discounted) + frequency_bonus(order_totals)
