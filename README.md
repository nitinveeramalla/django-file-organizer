# Django File Organizer

A simple Django app to organize files and view processing analytics.

## Quickstart (Windows PowerShell)

- **Prerequisites**: Python 3.10+ and pip
- **Project path**: `C:\Users\npuli\learning\django-file-organizer`

### 1) Create and activate a virtual environment
```powershell
cd C:\Users\npuli\learning\django-file-organizer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```powershell
pip install --upgrade pip
pip install django
```

### 3) Set up the database
```powershell
python manage.py migrate
```

### 4) Run the development server
```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## App URLs
- **Home**: `/`
- **Results (by session id)**: `/results/<session_id>/`
- **Analytics**: `/analytics/`
- **Admin (optional)**: `/admin/`

## Optional: Create an admin user
```powershell
python manage.py createsuperuser
```
Then sign in at `http://127.0.0.1:8000/admin/`.

## Running tests
```powershell
python manage.py test
```

## Notes
- Uses SQLite by default (`db.sqlite3` in the project root).
- Project URL routing is defined in `file_organizer/urls.py` and `organizer/urls.py`.

## Troubleshooting
- **Activate venv**: If commands use the wrong Python, re-run: `..\.venv\Scripts\Activate.ps1`.
- **Port in use**: Change port with `python manage.py runserver 8001`.
- **Migrations**: If models change, run `python manage.py makemigrations` then `python manage.py migrate`.
