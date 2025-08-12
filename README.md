# 🥭 Mango Shop API

A Django REST Framework (DRF) based e-commerce API for managing mango products, categories, carts, and orders.

## 🚀 Features
- **Category Management** – Organize mango varieties into categories.
- **Product Management** – Create, update, and list mango products with details like price and stock.
- **Cart System** – Add, update, and remove items from a user's cart.
- **Order Management** – Place orders, track statuses, and manage payments.
- **User Authentication** – Secure API endpoints with user accounts.
- **Order Items** – Track individual products within an order.

## 📂 Project Structure
project_root/
│
├── product/        # Manages mango categories and products
├── order/          # Handles carts, orders, and order items
├── user/           # User authentication and profiles
├── manage.py       # Django management script
└── requirements.txt

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL / SQLite (depending on config)
- **Authentication:** JWT / Session-based (depending on config)
- **Language:** Python 3.x

## ⚙️ Installation
1. Clone this repository:
   git clone https://github.com/yourusername/mango-shop.git
   cd mango-shop

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # Linux / Mac
   venv\Scripts\activate     # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Apply migrations:
   python manage.py migrate

5. Create a superuser:
   python manage.py createsuperuser

6. Run the development server:
   python manage.py runserver

## 📌 API Endpoints (Basic Overview)
- **Categories** – /api/categories/
- **Products** – /api/products/
- **Cart** – /api/cart/
- **Orders** – /api/orders/

## 📄 License
This project is licensed under the MIT License – feel free to modify and use it.

---
**Note:** This README is a starting point — update it with exact API details, authentication info, and deployment instructions.
