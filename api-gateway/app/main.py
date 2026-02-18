from fastapi import FastAPI, Request
import httpx
from pydantic import BaseModel
from fastapi import Header

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

app = FastAPI()

USER_SERVICE_URL = "http://127.0.0.1:8002"

@app.post("/register")
async def register(user: UserRegister):

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8002/register",
            json=user.dict()
        )

    return response.json()

@app.post("/login")
async def login(user: UserLogin):

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8002/login",
            json=user.dict()
        )

    return response.json()

@app.get("/products")
async def get_products(authorization: str = Header(None)):

    headers = {}
    if authorization:
        headers["Authorization"] = authorization

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8001/products",
            headers=headers
        )

    return response.json()