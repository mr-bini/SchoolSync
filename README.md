# 🏫 SchoolSync

**SchoolSync** is a minimal Django + DRF project that connects your static frontend pages to a powerful backend API with **JWT authentication** using **SimpleJWT**.  
It provides a clean and extendable foundation for building full-stack web applications with authentication, dashboards, and modular APIs.

---

## ⚙️ Features

- 🔹 Django + Django REST Framework backend  
- 🔹 JWT authentication using SimpleJWT  
- 🔹 Static frontend integration (HTML, CSS, JS)  
- 🔹 User registration, login, and dashboard redirect  
- 🔹 Extendable for future modules (homework, quizzes, schedules, etc.)

---

## 🧩 Requirements

Before you begin, make sure you have the following installed:

- **Python 3.9+**
- **pip** (Python package manager)
- **Git** (optional, for cloning the repository)

---

## 🚀 Installation Guide

### 🪟 Windows


# 1. Clone the repository

git clone https://github.com/yourusername/schoolsync.git
cd schoolsync

# 2. Create and activate a virtual environment

python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies

pip install -r requirements.txt

# 4. Apply migrations and create a superuser
python manage.py migrate
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver

🐧 Linux (Ubuntu / Debian)
# 1. Clone the repository
git clone https://github.com/yourusername/schoolsync.git
cd schoolsync

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations and create a superuser
python3 manage.py migrate
python3 manage.py createsuperuser

# 5. Run the development server
python3 manage.py runserver
🍎 macOS
# 1. Clone the repository
git clone https://github.com/yourusername/schoolsync.git
cd schoolsync

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations and create a superuser
python3 manage.py migrate
python3 manage.py createsuperuser

# 5. Run the development server
python3 manage.py runserver









