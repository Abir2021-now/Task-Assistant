# Task Assistant

Task Assistant is a Python-based task manager for creating, listing, completing, and deleting tasks. The project includes a command-line interface and a FastAPI API backed by SQLite.

## Recent changes

- Fixed runtime issues in the database and API layer
- Added task listing support required by the CLI and API
- Added validation for task titles, priorities, and IDs
- Added health and readiness endpoints
- Added request logging and security headers
- Added Docker and environment-based configuration
- Added tests and GitHub Actions CI workflow

## Features

- Create tasks with a title and priority (`high`, `medium`, or `low`)
- View all saved tasks
- Mark tasks as complete
- Delete tasks
- Access task data over HTTP
- Persist task data with SQLite
- Configure host, port, and CORS via environment variables

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
├── tests/
│   └── test_app.py
├── tasks.db
└── __pycache__/
```

## Requirements

```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables as needed:

```bash
DATABASE_NAME=tasks.db
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

## Run the CLI app

```bash
python main.py
```

## Run the API server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/ready`

## API endpoints

### `GET /`
Returns a simple service message.

### `GET /health`
Returns app health status.

### `GET /ready`
Returns readiness status.

### `GET /tasks`
Returns all tasks.

### `POST /tasks`
Creates a new task.

Example payload:

```json
{
  "title": "Write project documentation",
  "priority": "high"
}
```

### `GET /tasks/{task_id}`
Returns one task by ID.

### `PUT /tasks/{task_id}/complete`
Marks a task as complete.

### `DELETE /tasks/{task_id}`
Deletes a task.

## Example usage

```bash
curl http://127.0.0.1:8000/tasks
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Plan sprint work","priority":"high"}'
```

## Testing

```bash
pytest
```

## Docker

```bash
docker build -t task-assistant .
docker run -p 8000:8000 task-assistant
```

## Notes

- The app creates the SQLite database automatically when started.
- The repository now includes a stronger production-ready baseline with validation, config, and monitoring.
