import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4


DATA_DIR = Path(__file__).parent / "data"
ORDERS_FILE = DATA_DIR / "orders.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"
MESSAGES_FILE = DATA_DIR / "messages.json"


def _read_json(path):
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _write_json(path, data):
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def _price_to_float(price):
    return float(price.replace("$", ""))


def create_order(customer_name, email, flavor, scoops, toppings, pickup_time, notes):
    orders = _read_json(ORDERS_FILE)
    scoop_count = int(scoops)
    topping_count = len(toppings)
    total = (_price_to_float(flavor["price"]) * scoop_count) + (0.75 * topping_count)
    order = {
        "id": uuid4().hex[:8].upper(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "customer_name": customer_name,
        "email": email,
        "flavor_id": flavor["id"],
        "flavor_name": flavor["name"],
        "scoops": scoop_count,
        "toppings": toppings,
        "pickup_time": pickup_time,
        "notes": notes,
        "total": f"${total:.2f}",
        "status": "Received",
    }
    orders.append(order)
    _write_json(ORDERS_FILE, orders)
    return order


def get_orders():
    return list(reversed(_read_json(ORDERS_FILE)))


def get_order(order_id):
    for order in _read_json(ORDERS_FILE):
        if order["id"] == order_id:
            return order
    return None


def get_order_stats():
    orders = _read_json(ORDERS_FILE)
    revenue = sum(_price_to_float(order["total"]) for order in orders)
    return {
        "total_orders": len(orders),
        "estimated_revenue": f"${revenue:.2f}",
        "latest_order": orders[-1] if orders else None,
    }


def add_review(name, rating, favorite_flavor, comment):
    reviews = _read_json(REVIEWS_FILE)
    review = {
        "id": uuid4().hex[:8],
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "name": name,
        "rating": int(rating),
        "favorite_flavor": favorite_flavor,
        "comment": comment,
    }
    reviews.append(review)
    _write_json(REVIEWS_FILE, reviews)
    return review


def get_reviews():
    return list(reversed(_read_json(REVIEWS_FILE)))


def save_message(name, email, subject, message):
    messages = _read_json(MESSAGES_FILE)
    messages.append(
        {
            "id": uuid4().hex[:8],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
        }
    )
    _write_json(MESSAGES_FILE, messages)


def get_messages():
    return list(reversed(_read_json(MESSAGES_FILE)))
