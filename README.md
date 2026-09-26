# Afsha's Henna — Handcrafted Natural Henna & Supplies Website

A modern, mobile-first Django web application for **Afsha's Henna**, featuring bridal mehndi designs, organic henna cone sales, dynamic portfolio galleries, and direct WhatsApp ordering.

---

## 🌿 Features

- **Mobile-First Experience:** App-like bottom navigation dock with smooth page transitions.
- **Design Gallery:** Filterable portfolio showcasing Bridal, Arabic, Party, and Custom Henna art.
- **Product Catalog:** Direct ordering for fresh organic henna cones and pure supplies with live quantity & price estimation.
- **WhatsApp Integration:** Instant personalized inquiry messages generated for bookings and purchases.
- **Custom Admin Dashboard:** Powered by Django Jazzmin with easy management for designs, products, and site content.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd "henna website"
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
.\venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_data
```

### 5. Start the Development Server
```bash
python manage.py runserver
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🛠️ Tech Stack
- **Backend:** Python 3, Django 6.0
- **Admin Theme:** Django Jazzmin
- **Frontend:** Vanilla HTML5, CSS3 (Modern Responsive Design System), JavaScript ES6
- **Database:** SQLite (Default / Local)
