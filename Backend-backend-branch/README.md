# Backend — quick start (local, no Docker)

This README explains how to run the Python backend locally for development. It assumes you have Python 3.11+ installed.

1. Clone the repository and change to the backend folder

```powershell
git clone <repo-url>
cd <repo-folder>/Backend-backend-branch
```

2. Create and activate a virtual environment (Windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```powershell
pip install -r requirements.txt
```

4. Create your local `.env` from the example

```powershell
copy .env.example .env
# Edit .env to set SECRET_KEY and DATABASE_URL as needed
```

5. Initialize or migrate the database

```powershell
python migrate_db.py
# or: python init_db.py (project includes one of these)
```

6. Run the backend

```powershell
python main.py
# The backend should listen on the port defined in .env (default 8000)
```

Troubleshooting

- If you see missing package errors: ensure the venv is activated and `pip install -r requirements.txt` completed successfully.
- If DB errors occur: check `DATABASE_URL` in `.env` and run the migrate script.

If you'd like, I can now:

- add GitHub Actions CI that runs tests and linters for the backend
- scaffold a simple `init_db.py` seed script if you want shared sample data
