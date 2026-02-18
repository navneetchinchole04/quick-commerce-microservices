🚀 Quick Commerce Microservices

A full-stack Quick Commerce (Grocery Delivery) System built using a Microservices Architecture.

This project includes:

- 🔐 User Service (Authentication + JWT)

- 🛒 Cart Service

- 📦 Product Service

- 🚚 Delivery Service

- 🌐 API Gateway

- 🎯 Flutter Web Frontend

- 🐳 Dockerized services

- ☁️ MongoDB Atlas database

---

🏗️ Architecture

Flutter Frontend
        ↓
   API Gateway
        ↓
----------------------------------
| User | Product | Cart | Delivery |
----------------------------------
        ↓
    MongoDB Atlas

Each service runs independently in its own container.

---

🛠️ Tech Stack
Backend

- FastAPI

- MongoDB Atlas

- JWT Authentication

- Docker & Docker Compose

Frontend

- Flutter Web

DevOps

= Docker

- GitHub

---

📂 Project Structure

quick-commerce-app/
│
├── api-gateway/
├── user-service/
├── product-service/
├── cart-service/
├── delivery-service/
├── quick_commerce_app/   (Flutter frontend)
└── docker-compose.yml

---

⚙️ Setup Instructions

1️⃣ Clone Repository

git clone https://github.com/navneetchinchole04/quick-commerce-microservices.git
cd quick-commerce-microservices

---

2️⃣ Add Environment Variables

Create .env file inside:

- user-service

- product-service

Example:

MONGO_URL=your_mongodb_atlas_url
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256


⚠️ Do NOT commit .env files.

---

3️⃣ Run Backend Services

docker-compose up --build


Services will run on:

- User Service → http://localhost:8002

- Product Service → http://localhost:8001

- Cart Service → http://localhost:8003

- Delivery Service → http://localhost:8004

---

4️⃣ Run Flutter Frontend

cd quick_commerce_app
flutter run -d chrome

---

🔐 Authentication

Protected routes require JWT token.

Token is generated via User Service and passed in Authorization header:

Authorization: Bearer <token>

---

🧪 Sample Products

Example products:

Apple – ₹50

Banana – ₹30

Milk – ₹60

Bread – ₹40

---

🎥 Demo

Video demonstration will include:

- Microservices running via Docker

- API testing via browser / Swagger

- Flutter UI interaction

- Add to cart functionality

---

🌟 Key Features

✔ Microservices Architecture

✔ Secure JWT Authentication

✔ Dockerized Services

✔ Cloud Database (MongoDB Atlas)

✔ Flutter Web Frontend

✔ Clean Project Structure

---

👨‍💻 Author

Navneet Chinchole
B.Tech – Electronics & Computer Engineering
