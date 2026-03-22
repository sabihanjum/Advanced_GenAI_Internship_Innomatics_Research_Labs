from fastapi import FastAPI, Query, Response
from pydantic import BaseModel, Field
from typing import Optional
import math

app = FastAPI()

# =========================
# DATA
# =========================

menu = [
    {"id": 1, "name": "Pizza", "price": 250, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Burger", "price": 150, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Pasta", "price": 200, "category": "Pizza", "is_available": False},
    {"id": 5, "name": "Ice Cream", "price": 100, "category": "Dessert", "is_available": True},
    {"id": 6, "name": "Fries", "price": 120, "category": "Snack", "is_available": True},
]

orders = []
order_counter = 1

cart = []

# =========================
# HELPERS
# =========================

def find_menu_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None

def calculate_bill(price, quantity, order_type="delivery"):
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total

def filter_menu_logic(category=None, max_price=None, is_available=None):
    result = menu

    if category is not None:
        result = [i for i in result if i["category"].lower() == category.lower()]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]

    return result

# =========================
# PYDANTIC MODELS
# =========================

class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    item_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=20)
    delivery_address: str = Field(min_length=10)
    order_type: str = "delivery"

class NewMenuItem(BaseModel):
    name: str = Field(min_length=2)
    price: int = Field(gt=0)
    category: str = Field(min_length=2)
    is_available: bool = True

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

# =========================
# DAY 1 - GET APIs
# =========================

@app.get("/menu")
def get_menu():
    return {"items": menu, "total": len(menu)}

@app.get("/menu/summary")
def menu_summary():
    available = [i for i in menu if i["is_available"]]
    unavailable = [i for i in menu if not i["is_available"]]
    categories = list(set(i["category"] for i in menu))

    return {
        "total": len(menu),
        "available": len(available),
        "unavailable": len(unavailable),
        "categories": categories
    }

# ✅ FILTER
@app.get("/menu/filter")
def filter_menu(category: Optional[str] = None,
                max_price: Optional[int] = None,
                is_available: Optional[bool] = None):
    result = filter_menu_logic(category, max_price, is_available)
    return {"items": result, "count": len(result)}

# ✅ SEARCH (ADD THIS ABOVE)
@app.get("/menu/search")
def search_menu(keyword: str):
    result = [i for i in menu if keyword.lower() in i["name"].lower()]

    if not result:
        return {"message": "No items found"}

    return {"items": result, "total_found": len(result)}

# ✅ SORT (ADD THIS ABOVE)
@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    reverse = True if order == "desc" else False
    sorted_menu = sorted(menu, key=lambda x: x[sort_by], reverse=reverse)
    return {"items": sorted_menu}

# ✅ PAGINATION (ADD THIS ABOVE)
@app.get("/menu/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return {"items": menu[start:start + limit]}

# ✅ BROWSE (ADD THIS ABOVE)
@app.get("/menu/browse")
def browse():
    return {"items": menu}

@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}

# ❗ ALWAYS LAST
@app.get("/menu/{item_id}")
def get_item(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}
    return item

# =========================
# DAY 4 - CRUD
# =========================

@app.post("/menu")
def add_item(item: NewMenuItem, response: Response):
    for m in menu:
        if m["name"].lower() == item.name.lower():
            return {"error": "Item already exists"}

    new_item = item.dict()
    new_item["id"] = len(menu) + 1

    menu.append(new_item)
    response.status_code = 201
    return new_item

@app.put("/menu/{item_id}")
def update_item(item_id: int,
                price: Optional[int] = None,
                is_available: Optional[bool] = None):

    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item

@app.delete("/menu/{item_id}")
def delete_item(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}

    menu.remove(item)
    return {"message": f"{item['name']} deleted successfully"}

# =========================
# DAY 5 - CART WORKFLOW
# =========================

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)

    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Updated cart", "cart": cart}

    cart.append({
        "item_id": item_id,
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity
    })

    return {"message": "Added to cart", "cart": cart}

@app.get("/cart")
def view_cart():
    total = sum(i["price"] * i["quantity"] for i in cart)
    return {"cart": cart, "grand_total": total}

@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Item removed"}

    return {"error": "Item not in cart"}

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest, response: Response):
    global order_counter

    if not cart:
        return {"error": "Cart is empty"}

    created_orders = []
    total = 0

    for c in cart:
        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item": c["name"],
            "quantity": c["quantity"],
            "total_price": c["price"] * c["quantity"]
        }
        orders.append(order)
        created_orders.append(order)
        total += order["total_price"]
        order_counter += 1

    cart.clear()
    response.status_code = 201

    return {"orders": created_orders, "grand_total": total}

# =========================
# DAY 6 - ADVANCED
# =========================

@app.get("/menu/search")
def search_menu(keyword: str):
    result = [i for i in menu if keyword.lower() in i["name"].lower() or keyword.lower() in i["category"].lower()]

    if not result:
        return {"message": "No items found"}

    return {"items": result, "total_found": len(result)}

@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        return {"error": "Invalid sort field"}

    reverse = True if order == "desc" else False

    sorted_menu = sorted(menu, key=lambda x: x[sort_by], reverse=reverse)

    return {"sorted_by": sort_by, "order": order, "items": sorted_menu}

@app.get("/menu/page")
def paginate(page: int = Query(1, ge=1), limit: int = Query(3, ge=1, le=10)):
    start = (page - 1) * limit
    total = len(menu)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": math.ceil(total / limit),
        "items": menu[start:start + limit]
    }

@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]
    return {"results": result}

@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    reverse = True if order == "desc" else False
    sorted_orders = sorted(orders, key=lambda x: x["total_price"], reverse=reverse)
    return {"orders": sorted_orders}

@app.get("/menu/browse")
def browse(keyword: Optional[str] = None,
           sort_by: str = "price",
           order: str = "asc",
           page: int = 1,
           limit: int = 4):

    result = menu

    # filter
    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    # sort
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # pagination
    total = len(result)
    start = (page - 1) * limit

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": math.ceil(total / limit),
        "items": result[start:start + limit]
    }