"""Cosmic Pizza 🍕 — a tiny Flask app for building and pricing a pizza.

Run locally:
    pip install -r requirements.txt
    flask --app app run
Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template, request

from pizzeria.menu import SIZES, TOPPINGS, size_names, topping_names
from pizzeria.orders import Order
from pizzeria.pricing import format_price

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Render the pizza builder form."""
    return render_template(
        "index.html",
        sizes=size_names(),
        toppings=topping_names(),
        receipt=None,
    )


@app.route("/order", methods=["POST"])
def order():
    """Build an order from the submitted form and show a receipt."""
    size = request.form.get("size", "medium")
    selected = request.form.getlist("toppings")

    pizza = Order(size)
    for topping in selected:
        if topping in TOPPINGS:
            pizza.add_topping(topping)

    return render_template(
        "index.html",
        sizes=size_names(),
        toppings=topping_names(),
        receipt=pizza.receipt(),
    )


@app.route("/menu.json", methods=["GET"])
def menu_json():
    """Return the full menu as JSON, with prices formatted for display."""
    items = {}
    for name, details in TOPPINGS.items():
        items[name] = {
            "price": format_price(details["price"]),
            "calories": details["calories"],
            "category": details["category"],
        }
    return {
        "sizes": {name: format_price(price) for name, (price, _) in SIZES.items()},
        "toppings": items,
    }


if __name__ == "__main__":
    app.run(debug=True)
