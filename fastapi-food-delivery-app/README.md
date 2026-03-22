# FastAPI Food Delivery App

This is a backend project built using FastAPI as part of the internship final assignment.

## Project Overview

This project simulates a food delivery system where users can:
- View menu items
- Place orders
- Add items to cart
- Checkout orders
- Search, filter, sort, and paginate data

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic

## Features

### Day 1 - GET APIs
- Home route `/`
- Get all menu items `/menu`
- Get item by ID `/menu/{item_id}`
- Menu summary `/menu/summary`
- Get all orders `/orders`

### Day 2 - POST APIs
- Create order `/orders`
- Input validation using Pydantic

### Day 3 - Helpers & Filtering
- Helper functions:
  - find_menu_item()
  - calculate_bill()
  - filter_menu_logic()
- Filter API `/menu/filter`

### Day 4 - CRUD Operations
- Add item `/menu` (POST)
- Update item `/menu/{id}` (PUT)
- Delete item `/menu/{id}` (DELETE)

### Day 5 - Cart Workflow
- Add to cart `/cart/add`
- View cart `/cart`
- Remove item `/cart/{item_id}`
- Checkout `/cart/checkout`

### Day 6 - Advanced APIs
- Search `/menu/search`
- Sort `/menu/sort`
- Pagination `/menu/page`
- Combined browse `/menu/browse`
- Order search `/orders/search`
- Order sort `/orders/sort`

## Project Structure

fastapi-food-delivery-app/
- main.py
- requirements.txt
- README.md
- screenshots/
  - Q1.png
  - Q2.png
  - ...
  - Q20.png

## How to Run

1. Install dependencies:
pip install fastapi uvicorn

2. Run server:
python -m uvicorn main:app --reload

3. Open in browser:
http://127.0.0.1:8000/docs

## Screenshots

All API screenshots are stored in the screenshots folder.

## Acknowledgement

Thanks to Innomatics Research Labs for the learning opportunity.
