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

1️⃣ Clone the Repository
```bash
git clone https://github.com/mr-bini/SchoolSync.git
cd SchoolSync
```
2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
5️⃣ Create a Superuser
```bash
python manage.py createsuperuser
```
6️⃣ Run the Development Server
```bash
python manage.py runserver
```
Now open http://127.0.0.1:8000/ to access Schoolsync.

👨‍💻 Author
```
Biniyam Wondimu, Highschool student 💡 Aspiring System Architect | Backend Developer 📬 Building SchoolSync to Highschool students.
```
















