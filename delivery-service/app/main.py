from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
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

orders_collection = db["orders"]

# =============================
# Models
# =============================

class StatusUpdate(BaseModel):
    status: str


# =============================
# Routes
# =============================

@app.get("/")
def root():
    return {"message": "Delivery Service Running"}


# -----------------------------
# GET ORDER STATUS
# -----------------------------

@app.get("/order/{order_id}/status")
def get_order_status(order_id: str):

    order = orders_collection.find_one(
        {"order_id": order_id},
        {"_id": 0}
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_id": order_id,
        "status": order["status"],
        "last_updated": order.get("updated_at", order["created_at"])
    }


# -----------------------------
# UPDATE ORDER STATUS
# -----------------------------

@app.post("/order/{order_id}/update-status")
def update_status(order_id: str, data: StatusUpdate):

    valid_status = ["PLACED", "PACKED", "OUT_FOR_DELIVERY", "DELIVERED"]

    if data.status not in valid_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    result = orders_collection.update_one(
        {"order_id": order_id},
        {
            "$set": {
                "status": data.status,
                "updated_at": datetime.utcnow()
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": f"Order status updated to {data.status}"}
