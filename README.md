# Scoops & Smiles Flask App

Scoops & Smiles is a beginner-friendly ice cream shop web app built with Flask. It started as a simple routing/template project, then expanded into a complete student portfolio project with persistent JSON data, filtering, saved orders, reviews, contact messages, admin tools, and tests.

The goal is not to look like a senior engineering project. The goal is to show that a beginner coder can plan a real app, organize the files cleanly, use GET and POST correctly, pass data into templates, save data, style the pages, and test the most important behavior.

## Features

- Home page with shop statistics and the current featured flavor
- Flavors page with search, category filters, and dietary filters
- Flavor detail pages with ingredients, calories, tags, stock, and price
- Flavor of the Week page using simple date-based Python logic
- About page with FAQ content
- Contact form using `POST`, saved to `data/messages.json`
- Pickup order form using `POST`, saved to `data/orders.json`
- Review form using `POST`, saved to `data/reviews.json`
- Beginner-level admin dashboard with menu stats, order stats, messages, flavor add form, and availability toggle
- JSON-backed data storage
- Unit tests for GET pages, POST forms, search, admin actions, and saved JSON data

## Project Structure

```text
.
├── app.py
├── flavor_store.py
├── order_store.py
├── test_app.py
├── data/
│   ├── flavors.json
│   ├── messages.json
│   ├── orders.json
│   └── reviews.json
├── static/
│   └── style.css
├── templates/
│   ├── admin.html
│   ├── base.html
│   ├── contact.html
│   ├── flavor_detail.html
│   ├── flavor_of_the_week.html
│   ├── flavors.html
│   ├── home.html
│   ├── not_found.html
│   ├── order.html
│   ├── order_success.html
│   └── reviews.html
└── requirements.txt
```

## How to Run

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Flask:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
flask --app app run
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

## How to Test

```bash
python -m unittest
```

The tests use temporary JSON files so they do not overwrite the real project data.

## What This Demonstrates

- GET routes for normal pages
- POST routes for order, review, contact, and admin forms
- Dynamic URL routes like `/flavors/<flavor_id>` and `/order/<order_id>`
- Templates with data passed from Python
- Template inheritance through `base.html`
- Static CSS styling and responsive layouts
- JSON file reading/writing
- Search and filtering logic
- Basic validation before saving form submissions
- Separation between route code, flavor data logic, order/review/message logic, templates, and styles
- Automated route and behavior testing

## Why This Is Internship-Ready

This project is meant to feel impressive for a CS internship applicant because it goes beyond a tiny tutorial app, but it still uses beginner-friendly tools:

- Flask instead of a large backend framework
- JSON files instead of a full database
- Plain HTML templates instead of a frontend framework
- Simple forms instead of authentication, payments, or advanced APIs
- Small helper files instead of complicated architecture
- `unittest` tests that prove the main features work

It shows practical fundamentals without pretending to be production software.

## 100-Hour Project Reflection

This version is designed to reflect a larger beginner project timeline than a basic four-page Flask app. A realistic breakdown could look like this:

- 10 hours: planning the app, deciding pages, sketching data models, and organizing folders
- 15 hours: building Flask routes, templates, shared navigation, and base styling
- 12 hours: creating the flavor JSON data model with categories, tags, prices, calories, ingredients, and availability
- 12 hours: building search/filter behavior and individual flavor detail pages
- 14 hours: creating the order workflow, total calculation, confirmation pages, and saved order data
- 10 hours: building beginner admin dashboard features and flavor availability management
- 8 hours: adding reviews, contact messages, FAQ content, and extra user-facing pages
- 10 hours: improving CSS layout, mobile responsiveness, cards, forms, and dashboard sections
- 6 hours: writing automated tests for key GET/POST behavior
- 3 hours: documentation, cleanup, and final verification

That adds up to about 100 hours of project work and shows more than one beginner-to-intermediate skill area: backend routes, form handling, data persistence, templates, styling, testing, and documentation.

## What I Would Say in an Interview

I built this project to practice Flask fundamentals. I wanted it to be more than a static website, so I added real form submissions, JSON storage, search/filter logic, and an admin page. I kept the project beginner-friendly by using simple files and readable functions instead of jumping into databases or complex frameworks before I needed them.

If I had more time, I would improve the project by adding user login for the admin page, moving from JSON files to SQLite, and adding better form validation. I left those out because this version is focused on showing strong fundamentals clearly.
