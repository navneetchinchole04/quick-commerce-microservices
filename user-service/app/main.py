from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from passlib.context import CryptContext
from jose import jwt
import os

# =============================
# CONFIG
# =============================


MONGO_URL = os.getenv("MONGO_URL")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# =============================
# APP
# =============================

app = FastAPI()

client = MongoClient(MONGO_URL)
db = client["quick_commerce"]
users_collection = db["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =============================
# MODELS
# =============================

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# =============================
# ROOT
# =============================

@app.get("/")
def root():
    return {"message": "User Service Running"}

# =============================
# REGISTER
# =============================

@app.post("/register")
def register(user: UserRegister):

    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    })

    return {"message": "User registered successfully"}

# =============================
# LOGIN
# =============================

@app.post("/login")
def login(user: UserLogin):

    db_user = users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"sub": db_user["email"]},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}
