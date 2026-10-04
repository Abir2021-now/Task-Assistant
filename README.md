# Task Assistant

Task Assistant is a Python-based task manager for creating, listing, completing, and deleting tasks. The project includes a command-line interface and a FastAPI API backed by SQLite.

## Recent changes

- Step 10: Added optional API token authentication and a simple in-memory rate limiter for safer production behavior.
- Step 9: Added structured logging and security headers.
- Step 8: Added centralized configuration for runtime environment values.
- Step 7: Added request logging and CORS support.
- Step 6: Added Docker and environment-based deployment support.
- Step 5: Added database validation and safer task handling.
- Step 4: Added health and readiness endpoints.
- Step 3: Added stronger validation and delete support.
- Step 2: Added automated tests and CI.
- Step 1: Fixed the missing `get_tasks()` bug and added project setup files.

## Features

- Create and manage tasks with titles and priorities
- View and complete tasks
- Delete tasks
- Run as a CLI or API
- Store data in SQLite
- Environment-based configuration
- Request logging, security headers, optional auth, and rate limiting

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

## Configuration

Set environment variables as needed:

```bash
DATABASE_NAME=tasks.db
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000
API_TOKEN=your-secret-token
RATE_LIMIT=60
RATE_LIMIT_WINDOW_SECONDS=60
```

If `API_TOKEN` is set, every request must include:

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
curl -H "Authorization: Bearer your-secret-token" http://127.0.0.1:8000/tasks
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer your-secret-token" \
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
docker run -p 8000:8000 --env-file .env task-assistant
```

## Notes

- The app creates the SQLite database automatically when started.
- The repo now includes a stronger production baseline with validation, config, monitoring, and optional auth.
