# Task Assistant

Task Assistant is a Python-based task manager for creating, listing, completing, and deleting tasks. The project includes both an interactive command-line interface and a lightweight FastAPI API backed by SQLite.

## Recent changes

- Step 7: Added request logging and CORS support for safer production usage.
- Step 6: Added environment-based configuration and container support for easier deployment.
- Step 5: Added database validation for task titles, priorities, and IDs.
- Step 4: Added health and readiness endpoints to improve API operational monitoring.
- Step 3: Added stronger response models, validation, and a delete endpoint.
- Step 2: Added automated tests and CI.
- Step 1: Fixed the missing `database.get_tasks()` bug and added dependency management and project hygiene files.

## Features

- Create tasks with a title and priority (`high`, `medium`, or `low`)
- View all saved tasks
- Mark tasks as complete
- Delete tasks
- Access the data through a HTTP API
- Persist data using SQLite
- Run locally or in Docker
- Log requests and support browser-based clients via CORS

## Project structure

```text
.
├── app.py
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
├── tasks.db
└── __pycache__/
```

## Requirements

```bash
pip install -r requirements.txt
```

## Environment configuration

Create a `.env` file from `.env.example` if you want to override the default database path or host/port settings:

```bash
cp .env.example .env
```

Example values:

```env
DATABASE_NAME=tasks.db
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

## Run the CLI app

```bash
python main.py
```

## Run the API server locally

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/ready`

## Run with Docker

```bash
docker build -t task-assistant .
docker run -p 8000:8000 --env-file .env task-assistant
```

Or use Docker Compose:

```bash
docker-compose up --build
```

## API endpoints

### `GET /`
Returns a simple health message.

### `GET /health`
Returns app health.

### `GET /ready`
Returns readiness status.

### `GET /tasks`
Returns all tasks.

### `POST /tasks`
Creates a new task.

Example request body:

```json
{
  "title": "Write project documentation",
  "priority": "high"
}
```

### `GET /tasks/{task_id}`
Returns a specific task by ID.

### `PUT /tasks/{task_id}/complete`
Marks a task as completed.

### `DELETE /tasks/{task_id}`
Deletes a task by ID.

## Example usage

```bash
curl http://127.0.0.1:8000/tasks
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","priority":"medium"}'
```

## Testing

```bash
pytest
```

## CI

This repository includes a GitHub Actions workflow that runs the test suite automatically on pushes and pull requests.

## Notes

- The database file is created automatically when the app starts.
- Logging and CORS are enabled to support operational visibility and browser-based clients.
