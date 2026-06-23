import json
import tempfile
import unittest
from pathlib import Path

import flavor_store
import order_store
from app import app


class IceCreamAppTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)

        self.flavors_file = self.data_dir / "flavors.json"
        self.orders_file = self.data_dir / "orders.json"
        self.reviews_file = self.data_dir / "reviews.json"
        self.messages_file = self.data_dir / "messages.json"

        source_flavors = Path("data/flavors.json").read_text(encoding="utf-8")
        self.flavors_file.write_text(source_flavors, encoding="utf-8")
        self.orders_file.write_text("[]", encoding="utf-8")
        self.reviews_file.write_text("[]", encoding="utf-8")
        self.messages_file.write_text("[]", encoding="utf-8")

        self.original_paths = (
            flavor_store.DATA_FILE,
            order_store.ORDERS_FILE,
            order_store.REVIEWS_FILE,
            order_store.MESSAGES_FILE,
        )

        flavor_store.DATA_FILE = self.flavors_file
        order_store.ORDERS_FILE = self.orders_file
        order_store.REVIEWS_FILE = self.reviews_file
        order_store.MESSAGES_FILE = self.messages_file

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        (
            flavor_store.DATA_FILE,
            order_store.ORDERS_FILE,
            order_store.REVIEWS_FILE,
            order_store.MESSAGES_FILE,
        ) = self.original_paths
        self.temp_dir.cleanup()

    def test_get_pages_load(self):
        for path in [
            "/",
            "/flavors",
            "/flavor-of-the-week",
            "/about",
            "/contact",
            "/order",
            "/reviews",
            "/admin",
        ]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_flavor_search_and_detail(self):
        search_response = self.client.get("/flavors?q=mango&dietary=dairy-free")
        self.assertEqual(search_response.status_code, 200)
        self.assertIn(b"Mango Sorbet Splash", search_response.data)

        detail_response = self.client.get("/flavors/mango-sorbet-splash")
        self.assertEqual(detail_response.status_code, 200)
        self.assertIn(b"Flavor Details", detail_response.data)

    def test_order_post_saves_order(self):
        response = self.client.post(
            "/order",
            data={
                "customer_name": "Test Customer",
                "email": "test@example.com",
                "flavor_id": "mint-chip-chill",
                "scoops": "2",
                "toppings": ["Sprinkles", "Hot fudge"],
                "pickup_time": "15:30",
                "notes": "Extra napkins",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Order Received", response.data)

        orders = json.loads(self.orders_file.read_text(encoding="utf-8"))
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["flavor_name"], "Mint Chip Chill")
        self.assertEqual(orders[0]["total"], "$9.50")

    def test_admin_can_add_and_toggle_flavor(self):
        response = self.client.post(
            "/admin",
            data={
                "name": "Blueberry Crumble",
                "price": "$4.75",
                "description": "Blueberry ice cream with crumble pieces.",
                "category": "Premium",
                "tags": "vegetarian",
                "calories": "280",
                "ingredients": "Milk, cream, blueberries, crumble",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Blueberry Crumble was added", response.data)

        toggle_response = self.client.post(
            "/admin/flavors/blueberry-crumble/toggle",
            follow_redirects=True,
        )
        self.assertEqual(toggle_response.status_code, 200)

        added_flavor = flavor_store.get_flavor("blueberry-crumble")
        self.assertFalse(added_flavor["available"])

    def test_reviews_and_contact_are_saved(self):
        review_response = self.client.post(
            "/reviews",
            data={
                "name": "Sam",
                "rating": "5",
                "favorite_flavor": "Vanilla Bean Dream",
                "comment": "Great service.",
            },
            follow_redirects=True,
        )
        self.assertEqual(review_response.status_code, 200)

        contact_response = self.client.post(
            "/contact",
            data={
                "name": "Sam",
                "email": "sam@example.com",
                "subject": "Birthday order",
                "message": "Can I order ahead?",
            },
        )
        self.assertEqual(contact_response.status_code, 200)

        reviews = json.loads(self.reviews_file.read_text(encoding="utf-8"))
        messages = json.loads(self.messages_file.read_text(encoding="utf-8"))
        self.assertEqual(len(reviews), 1)
        self.assertEqual(len(messages), 1)


if __name__ == "__main__":
    unittest.main()
