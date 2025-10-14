# SchoolSync (minimal Django + DRF starter)

This workspace contains a minimal Django project scaffolding to connect your existing static frontend pages to a Django + DRF backend with JWT authentication (SimpleJWT).

Quick start (Windows PowerShell):

1. Create and activate a virtual environment

   python -m venv venv; .\venv\Scripts\Activate.ps1

2. Install requirements

   pip install -r requirements.txt

3. Run migrations and create a superuser

   python manage.py migrate; python manage.py createsuperuser

4. Run the dev server

   python manage.py runserver

Open http://127.0.0.1:8000/ to see the login page. Signup posts to /api/auth/register and Login to /api/auth/login (SimpleJWT token pair). After login you'll be redirected to /dashboard/.

Notes:
- This is a minimal starter. Token blacklist for logout isn't configured (logout simply removes tokens client-side).
- Adjust SECRET_KEY and DEBUG in `schoolsync/settings.py` for production.
