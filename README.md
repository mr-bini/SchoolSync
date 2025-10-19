

# 🏫 **SchoolSync – Smart Collaboration Platform for High School Students**

**SchoolSync** is a modern web-based platform designed to help high school students organize study groups, manage homework, share notes, and stay connected through challenges and events.
It unifies all academic and social collaboration features in one place — bridging communication gaps between students, study teams, and mentors.

---

## 📖 Table of Contents

1. Overview
2. Features
3. Architecture
4. Tech Stack
5. Installation & Setup
6. API Endpoints
7. Authentication Flow
8. Project Structure
9. Roadmap
10. Author

---

## 🧩 Overview

**SchoolSync** was built to:

* Empower students to collaborate efficiently and manage academic workloads
* Provide a central space for **notes, schedules, quizzes, and study groups**
* Enable healthy academic competition through **quizzes and leaderboards**
* Replace scattered tools (social apps, notebooks, reminders) with a single smart platform

The project follows a modular **Django + REST API architecture**, with a responsive **frontend** built using Django templates and JavaScript-based interactivity.

---

## ✨ Features (Current Stage)

| Category            | Description                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| **User Management** | Custom Django user model with registration, login, and profile management                      |
| **Groups**          | Create and join study groups; exchange group messages                                          |
| **Homework Notes**  | Post, view, like, and comment on study notes                                                   |
| **Quizzes**         | Create, take, and track quizzes; folder-based organization; leaderboard & history              |
| **Schedule**        | Manage personal or group events (create/edit/delete)                                           |
| **Dashboard**       | Unified view of stats, quick notes, and notifications                                          |
| **API-Ready**       | Fully RESTful API endpoints for all entities (groups, notes, quizzes, schedule, notifications) |

---

## 🏗️ Architecture

### 🗂 App Structure

```
api/                 → Backend logic: models, views, serializers, and endpoints
templates/           → Frontend templates for dashboard, groups, quizzes, schedule, etc.
static/              → CSS, JS, and icons
schoolsync/          → Core Django configuration (settings, urls, middleware)
manage.py            → Project runner
```

### 🗄️ Database Models

| Model             | Description                                                               |
| ----------------- | ------------------------------------------------------------------------- |
| **User**          | Handles authentication and profile data                                   |
| **Group**         | Represents study groups with join/leave capability                        |
| **Message**       | Group messages between users                                              |
| **HomeworkNote**  | Notes shared among students with likes & comments                         |
| **Quiz**          | Each quiz belongs to a folder and stores questions, answers, and attempts |
| **QuizFolder**    | Organizes quizzes under a category/folder                                 |
| **ScheduleEvent** | User-specific events and reminders                                        |

---

## 🧠 Tech Stack

| Layer               | Technology                                            |
| ------------------- | ----------------------------------------------------- |
| **Backend**         | Django + Django REST Framework                        |
| **Frontend**        | Django Templates + JavaScript (Vanilla)               |
| **Database**        | SQLite (dev) → PostgreSQL (production)                |
| **Auth**            | Django session-based (CSRF + credentials:same-origin) |
| **Styling**         | HTML5, CSS3, Boxicons                                 |
| **Version Control** | Git + GitHub                                          |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mr-bini/SchoolSync.git
cd SchoolSync
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a Superuser

```bash
python manage.py createsuperuser
```

### 6️⃣ Run the Development Server

```bash
python manage.py runserver
```

Now open [http://127.0.0.1:8000](http://127.0.0.1:8000) to access **SchoolSync**.

---

## 🔑 API Endpoints

### 👥 Authentication

| Method | Endpoint                  | Description                  |
| ------ | ------------------------- | ---------------------------- |
| POST   | `/api/auth/register`      | Register a new user          |
| POST   | `/api/auth/login`         | Log in and start a session   |
| POST   | `/api/auth/logout`        | Log out current user         |
| POST   | `/api/auth/token/refresh` | Refresh authentication token |

---

### 🧑‍🎓 Users & Groups

| Method   | Endpoint                    | Description            |
| -------- | --------------------------- | ---------------------- |
| GET/POST | `/api/groups`               | List or create groups  |
| POST     | `/api/groups/<id>/join`     | Join a group           |
| POST     | `/api/groups/<id>/leave`    | Leave a group          |
| DELETE   | `/api/groups/<id>/delete`   | Delete a group         |
| PUT      | `/api/groups/<id>/edit`     | Edit group details     |
| GET/POST | `/api/groups/<id>/messages` | Send or fetch messages |

---

### 📝 Homework Notes

| Method     | Endpoint                      | Description             |
| ---------- | ----------------------------- | ----------------------- |
| GET/POST   | `/api/homework`               | Create or list notes    |
| GET/DELETE | `/api/homework/<id>`          | Retrieve or delete note |
| POST       | `/api/homework/<id>/like`     | Like a note             |
| POST       | `/api/homework/<id>/comments` | Add a comment           |
| DELETE     | `/api/homework/comments/<id>` | Delete a comment        |

---

### 🎯 Quizzes

| Method   | Endpoint                        | Description            |
| -------- | ------------------------------- | ---------------------- |
| GET/POST | `/api/quizzes`                  | List or create quizzes |
| GET      | `/api/quizzes/<id>`             | Retrieve quiz details  |
| POST     | `/api/quizzes/<id>/attempt`     | Submit a quiz attempt  |
| GET      | `/api/quizzes/<id>/leaderboard` | View quiz leaderboard  |
| GET      | `/api/quizzes/my-activity`      | User’s quiz history    |

---

### 📂 Quiz Folders

| Method         | Endpoint                            | Description            |
| -------------- | ----------------------------------- | ---------------------- |
| GET/POST       | `/api/quizzes/folders`              | List or create folders |
| GET/PUT/DELETE | `/api/quizzes/folders/<id>`         | Manage folder          |
| GET            | `/api/quizzes/folders/<id>/quizzes` | Quizzes in folder      |

---

### 📅 Schedule

| Method         | Endpoint              | Description           |
| -------------- | --------------------- | --------------------- |
| GET/POST       | `/api/schedule/`      | List or create events |
| GET/PUT/DELETE | `/api/schedule/<id>/` | Manage specific event |


---

## 🔒 Authentication Flow

1. User logs in via the login page (`/login/`)
2. Session cookies + CSRF token manage secure access
3. All API calls include:

   ```js
   fetch(url, {
     credentials: 'same-origin',
     headers: { 'X-CSRFToken': csrftoken }
   })
   ```
4. Unauthorized access returns 401/403 → redirected to `/login/`

---

## 📂 Project Structure

```
schoolsync/
├── api/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── migrations/
├── templates/
│   ├── home.html
│   ├── dashboard.html
│   ├── groups.html
│   ├── quizzes.html
│   ├── schedule.html
│   └── homework.html
├── static/
│   └── home/style.css
├── schoolsync/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

---

## 🧭 Roadmap (Next Steps)

| Feature             | Description                              | Status         |
| ------------------- | ---------------------------------------- | -------------- |
| Dashboard           | Stats + quick notes                      | 🟢 Implemented |
| Quizzes             | Folder, attempt, leaderboard             | 🟢 Implemented |
| Schedule            | Calendar + CRUD events                   | 🟢 Implemented |
| Group Chats         | Study group collaboration                | 🟢 Implemented |
| User Profiles       | Profile editing and avatars              | ⚪ Planned      |
| Real-Time Updates   | WebSocket integration                    | ⚪ Planned      |
| Mobile Optimization | Responsive redesign                      | ⚪ Planned      |
| Notifications       | Alerts for new events, homework, quizzes | ⚪ Planned      |


---

## 👨‍💻 Author

**Biniyam Wondimu**
💻 Full-Stack Developer | ALX Software Engineering Student
🌍 Building **SchoolSync** to make studying smarter, together.
📬 [GitHub](https://github.com/mr-bini) | [LinkedIn](https://www.linkedin.com/in/biniyam-wondimu-12620b327) | 



