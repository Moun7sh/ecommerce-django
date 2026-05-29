# 🏆 Sports Store - Django E-Commerce Website

A Django-based e-commerce web application for selling sports products online. The project allows users to browse products, manage their shopping cart, and provides an admin panel for product management.

## 🚀 Features

- Browse sports products
- View product details
- Add products to cart
- Update cart quantities
- Remove items from cart
- Session-based shopping cart
- Django Admin Dashboard
- SQLite database integration
- Responsive user interface

## 🛠️ Tech Stack

- Python
- Django
- HTML5
- CSS3
- SQLite3
- Pillow

## 📁 Project Structure

```text
sports-store/
│
├── config/
├── store/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── cart.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Moun7sh/sports-store.git
cd sports-store
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install django pillow
```

Run migrations:

```bash
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

Start server:

```bash
python manage.py runserver
```

Visit:

```text
http://127.0.0.1:8000/
```

## 🔑 Admin Access

```text
http://127.0.0.1:8000/admin/
```

Manage products, inventory, and store data through Django Admin.

## 🎯 Future Improvements

- User Authentication
- Product Categories
- Search Functionality
- Wishlist
- Payment Gateway Integration
- Order Management
- Product Reviews & Ratings

## 📚 Learning Objectives

This project was built to practice:

- Django Models
- Django Views
- URL Routing
- Template Rendering
- Session Management
- Shopping Cart Implementation
- Database Operations
- Django Admin Customization

## 👨‍💻 Author

**Moun7sh**

GitHub: https://github.com/Moun7sh

## 📄 License

This project is open-source and available under the MIT License.
