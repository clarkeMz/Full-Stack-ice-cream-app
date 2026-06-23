from flask import Flask, redirect, render_template, request, url_for

from flavor_store import (
    add_flavor,
    get_available_flavors,
    get_categories,
    get_flavor,
    get_flavor_of_the_week,
    get_flavors,
    get_menu_stats,
    search_flavors,
    toggle_availability,
)
from order_store import (
    add_review,
    create_order,
    get_messages,
    get_order,
    get_order_stats,
    get_orders,
    get_reviews,
    save_message,
)


app = Flask(__name__)

TOPPINGS = [
    "Sprinkles",
    "Hot fudge",
    "Whipped cream",
    "Caramel drizzle",
    "Chocolate chips",
    "Fresh strawberries",
]


@app.route("/")
def home():
    featured_flavor = get_flavor_of_the_week()
    reviews = get_reviews()[:2]
    stats = get_menu_stats()
    return render_template(
        "home.html",
        featured_flavor=featured_flavor,
        reviews=reviews,
        stats=stats,
    )


@app.route("/flavors")
def flavors():
    search_term = request.args.get("q", "").strip()
    category = request.args.get("category", "all")
    dietary = request.args.get("dietary", "all")
    flavor_list = search_flavors(search_term, category, dietary)

    return render_template(
        "flavors.html",
        flavors=flavor_list,
        categories=get_categories(),
        search_term=search_term,
        selected_category=category,
        selected_dietary=dietary,
    )


@app.route("/flavors/<flavor_id>")
def flavor_detail(flavor_id):
    flavor = get_flavor(flavor_id)
    if flavor is None:
        return render_template("not_found.html", item="flavor"), 404
    return render_template("flavor_detail.html", flavor=flavor)


@app.route("/flavor-of-the-week")
def flavor_of_the_week():
    flavor = get_flavor_of_the_week()
    return render_template("flavor_of_the_week.html", flavor=flavor)


@app.route("/about")
def about():
    faqs = [
        {
            "question": "Do you have dairy-free options?",
            "answer": "Yes. Use the dairy-free filter on the flavors page.",
        },
        {
            "question": "Can I place an order online?",
            "answer": "Yes. The order form saves each order to a JSON file.",
        },
        {
            "question": "What does the admin page show?",
            "answer": "It lists orders, messages, menu stats, and a form for adding flavors.",
        },
    ]
    return render_template("about.html", faqs=faqs)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if name and email and subject and message:
            save_message(name, email, subject, message)
            return render_template("contact.html", success=True)

        return render_template("contact.html", error="Please complete every field.")

    return render_template("contact.html")


@app.route("/order", methods=["GET", "POST"])
def order():
    flavors = get_available_flavors()

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        email = request.form.get("email", "").strip()
        flavor_id = request.form.get("flavor_id", "").strip()
        scoops = request.form.get("scoops", "1")
        toppings = request.form.getlist("toppings")
        pickup_time = request.form.get("pickup_time", "").strip()
        notes = request.form.get("notes", "").strip()
        flavor = get_flavor(flavor_id)

        if not all([customer_name, email, flavor, scoops, pickup_time]):
            return render_template(
                "order.html",
                flavors=flavors,
                toppings=TOPPINGS,
                error="Please complete the required order fields.",
            )

        order_data = create_order(
            customer_name,
            email,
            flavor,
            scoops,
            toppings,
            pickup_time,
            notes,
        )
        return redirect(url_for("order_success", order_id=order_data["id"]))

    return render_template("order.html", flavors=flavors, toppings=TOPPINGS)


@app.route("/order/<order_id>")
def order_success(order_id):
    order_data = get_order(order_id)
    if order_data is None:
        return render_template("not_found.html", item="order"), 404
    return render_template("order_success.html", order=order_data)


@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        rating = request.form.get("rating", "5")
        favorite_flavor = request.form.get("favorite_flavor", "").strip()
        comment = request.form.get("comment", "").strip()

        if name and favorite_flavor and comment:
            add_review(name, rating, favorite_flavor, comment)
            return redirect(url_for("reviews"))

        return render_template(
            "reviews.html",
            reviews=get_reviews(),
            flavors=get_flavors(),
            error="Please complete every review field.",
        )

    return render_template("reviews.html", reviews=get_reviews(), flavors=get_flavors())


@app.route("/admin", methods=["GET", "POST"])
def admin():
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price = request.form.get("price", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        tag_text = request.form.get("tags", "").strip()
        calories = request.form.get("calories", "").strip()
        ingredients = request.form.get("ingredients", "").strip()
        tags = [tag.strip() for tag in tag_text.split(",") if tag.strip()]

        if name and price and description and category and calories and ingredients:
            add_flavor(name, price, description, category, tags, calories, ingredients)
            return redirect(url_for("admin", added=name))

        message = "Please fill in every field before adding a flavor."

    return render_template(
        "admin.html",
        flavors=get_flavors(),
        orders=get_orders(),
        messages=get_messages(),
        menu_stats=get_menu_stats(),
        order_stats=get_order_stats(),
        message=message,
        added=request.args.get("added"),
    )


@app.route("/admin/flavors/<flavor_id>/toggle", methods=["POST"])
def admin_toggle_flavor(flavor_id):
    toggle_availability(flavor_id)
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
