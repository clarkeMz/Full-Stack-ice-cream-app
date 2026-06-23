import json
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "flavors.json"


def _slugify(text):
    return (
        text.lower()
        .replace("&", "and")
        .replace(" ", "-")
        .replace("'", "")
    )


def get_flavors():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_flavors(flavors):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(flavors, file, indent=2)


def get_available_flavors():
    return [flavor for flavor in get_flavors() if flavor.get("available", True)]


def get_flavor(flavor_id):
    for flavor in get_flavors():
        if flavor["id"] == flavor_id:
            return flavor
    return None


def get_categories():
    categories = {flavor["category"] for flavor in get_flavors()}
    return sorted(categories)


def search_flavors(search_term="", category="all", dietary="all"):
    search_text = search_term.lower()
    matching_flavors = []

    for flavor in get_flavors():
        fields_to_search = [
            flavor["name"],
            flavor["description"],
            flavor["category"],
            " ".join(flavor.get("tags", [])),
        ]
        matches_search = not search_text or any(
            search_text in field.lower() for field in fields_to_search
        )
        matches_category = category == "all" or flavor["category"] == category
        matches_dietary = dietary == "all" or dietary in flavor.get("tags", [])

        if matches_search and matches_category and matches_dietary:
            matching_flavors.append(flavor)

    return matching_flavors


def get_flavor_of_the_week():
    flavors = get_available_flavors()
    week_number = date.today().isocalendar().week
    flavor_index = week_number % len(flavors)
    return flavors[flavor_index]


def add_flavor(name, price, description, category, tags, calories, ingredients):
    flavors = get_flavors()
    flavors.append(
        {
            "id": _slugify(name),
            "name": name,
            "price": price,
            "description": description,
            "category": category,
            "tags": tags,
            "calories": calories,
            "ingredients": ingredients,
            "available": True,
            "stock": 24,
            "featured_note": "A new shop-made recipe added from the admin page.",
        }
    )
    save_flavors(flavors)


def toggle_availability(flavor_id):
    flavors = get_flavors()
    for flavor in flavors:
        if flavor["id"] == flavor_id:
            flavor["available"] = not flavor.get("available", True)
            save_flavors(flavors)
            return flavor
    return None


def get_menu_stats():
    flavors = get_flavors()
    available_count = len([flavor for flavor in flavors if flavor.get("available", True)])
    categories = get_categories()

    return {
        "total_flavors": len(flavors),
        "available_flavors": available_count,
        "category_count": len(categories),
        "categories": categories,
    }
