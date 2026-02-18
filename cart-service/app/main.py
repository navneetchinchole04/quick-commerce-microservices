from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pymongo import MongoClient
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid
import os

# =============================
# App Setup
# =============================

app = FastAPI()

# =============================
# MongoDB Setup
# =============================


MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["quick_commerce"]

cart_collection = db["cart"]
orders_collection = db["orders"]

# =============================
# JWT Setup (same as user service)
# =============================

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# =============================
# Models
# =============================

class CartItem(BaseModel):
    product_id: str
    quantity: int
    price: float


# =============================
# Routes
# =============================

@app.get("/")
def root():
    return {"message": "Cart & Order Service Running"}


# -----------------------------
# ADD TO CART
# -----------------------------

@app.post("/cart/add")
def add_to_cart(item: CartItem, current_user: dict = Depends(get_current_user)):

    user_id = current_user["id"]

    existing = cart_collection.find_one({
        "user_id": user_id,
        "product_id": item.product_id
    })

    if existing:
        cart_collection.update_one(
            {"_id": existing["_id"]},
            {"$inc": {"quantity": item.quantity}}
        )
    else:
        cart_collection.insert_one({
            "user_id": user_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price
        })

    return {"message": "Item added to cart"}


# -----------------------------
# VIEW CART
# -----------------------------

@app.get("/cart")
def view_cart(current_user: dict = Depends(get_current_user)):

    user_id = current_user["id"]

    items = list(cart_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ))

    return items


# -----------------------------
# REMOVE ITEM
# -----------------------------

@app.delete("/cart/remove/{product_id}")
def remove_item(product_id: str, current_user: dict = Depends(get_current_user)):

    user_id = current_user["id"]

    result = cart_collection.delete_one({
        "user_id": user_id,
        "product_id": product_id
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item removed"}


# -----------------------------
# CREATE ORDER
# -----------------------------

@app.post("/order/create")
def create_order(current_user: dict = Depends(get_current_user)):

    user_id = current_user["id"]

    cart_items = list(cart_collection.find({"user_id": user_id}))

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0
    order_items = []

    for item in cart_items:
        total_amount += item["price"] * item["quantity"]
        order_items.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": item["price"]
        })

    order_id = str(uuid.uuid4())

    order_data = {
        "order_id": order_id,
        "user_id": user_id,
        "items": order_items,
        "total_amount": total_amount,
        "status": "PLACED",
        "created_at": datetime.utcnow()
    }

    orders_collection.insert_one(order_data)

    # Clear cart after order
    cart_collection.delete_many({"user_id": user_id})

    return {
        "message": "Order created successfully",
        "order_id": order_id,
        "total_amount": total_amount
    }


# -----------------------------
# GET ORDERS
# -----------------------------

@app.get("/orders")
def get_orders(current_user: dict = Depends(get_current_user)):

    user_id = current_user["id"]

    orders = list(orders_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ))

    return orders
