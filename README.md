# Scoops & Smiles Flask App

Scoops & Smiles is a ice cream shop web app built with Flask. It started as a simple routing/template project, then expanded into a complete student portfolio project with persistent JSON data, filtering, saved orders, reviews, contact messages, admin tools, and tests.

## Features

- Home page with shop statistics and the current flavor
- Flavors page with search, category filters, and dietary filters
- Flavor pages with ingredients, calories, tags, stock, and price
- Flavor of the Week page 
- Unit tests for GET pages, POST forms, search, admin actions, and saved JSON data

## Project Structure
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

## How to Test

```bash
python -m unittest
```



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
