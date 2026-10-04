# Task Assistant

Task Assistant is a Python-based task manager for creating, listing, completing, and deleting tasks. The project includes a command-line interface and a FastAPI API backed by SQLite or PostgreSQL.

## Recent changes

- PostgreSQL-ready architecture added with SQLAlchemy and Alembic migration support.
- Optional API authentication and rate limiting added for secure production use.
- Added request logging, health checks, and environment-driven runtime config.
- Added Docker and CI support.

## Features

- Create tasks with a title and priority (`high`, `medium`, or `low`)
- View all saved tasks
- Mark tasks as complete
- Delete tasks
- Expose REST API endpoints
- Persist data using SQLite by default, or PostgreSQL via `DATABASE_URL`
- Run with Docker and environment variables
- Optional bearer-token auth and rate limiting

## Project structure

```text
.
├── app.py
├── database.py
├── settings.py
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
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 20241004_create_tasks_table.py
├── tests/
│   └── test_app.py
├── tasks.db
└── __pycache__/
```

## Configuration

Use environment variables to configure the app:

```bash
DATABASE_URL=sqlite:///./tasks.db
DATABASE_NAME=tasks.db
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000
API_TOKEN=your-secret-token
RATE_LIMIT=60
RATE_LIMIT_WINDOW_SECONDS=60
```

For PostgreSQL:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskassistant
```

If `API_TOKEN` is set, requests must include:

```bash
Authorization: Bearer your-secret-token
```

## Run the CLI app

```bash
python main.py
```

## Run the API server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Alembic migrations

Create the migration database and run upgrades:

```bash
alembic upgrade head
```

If you need a new migration:

```bash
alembic revision --autogenerate -m "describe your change"
```

## Health endpoints

- `/health`
- `/ready`
- `/docs`

## Testing

```bash
pytest
```
