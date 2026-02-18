from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env from parent directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["product_db"]
products_collection = db["products"]

sample_products = [
    {
        "name": "Milk",
        "description": "Fresh dairy milk",
        "price": 50,
        "category": "Dairy",
        "image_url": "https://via.placeholder.com/150",
        "available": True
    },
    {
        "name": "Bread",
        "description": "Whole wheat bread",
        "price": 40,
        "category": "Bakery",
        "image_url": "https://via.placeholder.com/150",
        "available": True
    },
    {
        "name": "Apple",
        "description": "Fresh red apples",
        "price": 120,
        "category": "Fruits",
        "image_url": "https://via.placeholder.com/150",
        "available": True
    }
]

products_collection.insert_many(sample_products)

print("Sample products inserted successfully")
