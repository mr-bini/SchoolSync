# 🏫 SchoolSync

**SchoolSync**  is a web-based platform designed to help high school students:
- 🔹 Organize study groups.
- 🔹 Track homework and deadlines.
- 🔹 Share notes with classmates.
- 🔹 Play fun quizzes and challenges.
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
```bash
git clone https://github.com/mr-bini/SchoolSync.git
cd schoolsync
```
# 2. Create and activate a virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```
# 3. Install dependencies
```bash
pip install -r requirements.txt
```
# 4. Apply migrations and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```
# 5. Run the development server
```bash
python manage.py runserver
```
🐧 Linux (Ubuntu / Debian)
# 1. Clone the repository
```bash
git clone https://github.com/mr-bini/SchoolSync.git
cd schoolsync
```
# 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
# 3. Install dependencies
```bash
pip install -r requirements.txt
```
# 4. Apply migrations and create a superuser
```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```
# 5. Run the development server
```bash
python3 manage.py runserver
```
🍎 macOS
# 1. Clone the repository
```bash
git clone https://github.com/mr-bini/SchoolSync.git
cd schoolsync
```
# 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
# 3. Install dependencies
```bash
pip install -r requirements.txt
```
# 4. Apply migrations and create a superuser
```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```
# 5. Run the development server
```bash
python3 manage.py runserver
```



















