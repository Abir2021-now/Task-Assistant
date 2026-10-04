# Task Assistant

Task Assistant is a Python-based task manager for creating, listing, completing, and deleting tasks. The project includes an interactive command-line interface and a FastAPI API backed by SQLite.

## Recent changes

- Step 8: Added a central settings module to make runtime configuration environment-based and cleaner for deployment.
- Step 7: Added request logging and CORS support.
- Step 6: Added Docker and environment-driven deployment support.
- Step 5: Added database validation and safer task handling.
- Step 4: Added health and readiness endpoints.
- Step 3: Added stronger API validation and delete support.
- Step 2: Added automated tests and CI.
- Step 1: Fixed the missing `get_tasks()` bug and added project setup files.

## Features

- Create and manage tasks with titles and priorities
- View and complete tasks
- Delete tasks
- Run as a CLI or API
- Store data in SQLite
- Environment-based configuration for host, port, and CORS

## Project structure

```text
.
├── app.py
├── settings.py
├── database.py
├── main.py
├── models.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── CHANGELOG.md
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_app.py
└── tasks.db
```

## Config

Use environment variables to control runtime behavior:

```bash
DATABASE_NAME=tasks.db
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

## Run the CLI

```bash
python main.py
```

## Run the API

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Health endpoints

- `/health`
- `/ready`
- `/docs`

## Testing

```bash
pytest
```
