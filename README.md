# VC Food — Django Food Ordering Website

A simple food ordering site built with Django, Bootstrap, and SQLite (MySQL-ready).Supports menu browsing, cart, checkout, order history, wishlist, and user authentication.


## Features
- Menu, cart, checkout, order summary/history
- Built-in auth + signup
- Django admin for dish and orders management


## 📦 Features
## 🍽 Menu & Food Ordering

- View dishes and categories

- Dish details page

- Add/remove items from cart

- Wishlist support

## 🛒 Checkout & Orders

- Order summary

- Payment placeholder (extendable)

- Order history per user

## 👤 Authentication

- Django Allauth-style login/signup

- Password reset

- Admin panel

## ⚙️ Admin

- Add/edit/delete dishes

- Manage categories

- Manage user orders

## Quickstart

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations and create a superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

Visit `/admin/` for admin, `/accounts/login/` to log in, and `/` for the menu.


💾 Default Database (SQLite)

The project uses SQLite during development for simplicity.
To use MySQL, review the section below.


## Switch to MySQL later
- Install `mysqlclient`
- Set environment variables (e.g., in your shell):
  - `DB_ENGINE=mysql`
  - `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`
- Run migrations again.