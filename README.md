# Personal Finance Tracker (minimal)

This is a minimal Django + DRF project (SQLite) with a simple frontend (Chart.js) for a personal finance tracker.

## Quick start (Windows / VS Code)
1. Extract the ZIP.
2. Open folder in VS Code.
3. Create & activate a virtualenv:
   ```
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Make migrations and migrate:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create superuser:
   ```
   python manage.py createsuperuser
   ```
6. Run server:
   ```
   python manage.py runserver
   ```
7. Open dashboard:
   http://127.0.0.1:8000/dashboard/

APIs:
- /api/categories/
- /api/transactions/
- /api/reports/category_breakdown/

Notes:
- This project uses SQLite by default for zero setup.
- The dashboard uses session authentication (login via Django admin or standard auth).
