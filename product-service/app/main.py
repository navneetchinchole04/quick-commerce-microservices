from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path
from bson import ObjectId
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware

# Load environment
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URL = os.getenv("MONGO_URL")
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MongoDB Setup ----------------
client = MongoClient(MONGO_URL)
db = client["product_db"]
products_collection = db["products"]

# ---------------- Security Setup ----------------
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ---------------- Routes ----------------

@app.get("/")
def root():
    return {"message": "Product Service Running Successfully"}


# 🔐 PROTECTED PRODUCTS ROUTE
@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Apple", "price": 50},
        {"id": 2, "name": "Banana", "price": 30},
        {"id": 3, "name": "Milk", "price": 60},
        {"id": 4, "name": "Bread", "price": 40}
    ]


@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = products_collection.find_one({"_id": ObjectId(product_id)})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product["_id"] = str(product["_id"])
    return product
