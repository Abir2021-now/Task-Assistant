# Task Assistant

Task Assistant is a Python-based task manager designed for simple local task tracking. The project includes both a CLI and a FastAPI API, and it stores data in a SQLite database.

## Recent changes

This update is part of Step 1 of the production-readiness work.

- Fixed the missing `database.get_tasks()` function required by the CLI and API
- Added a proper dependency list for reproducible setup
- Added project hygiene files (`.gitignore`, `LICENSE`)
- Improved the CLI delete flow to validate task IDs before deletion
- Refreshed the documentation to reflect the actual app behavior

## Features

- Add tasks with a title and priority (`high`, `medium`, `low`)
- View all tasks
- Mark tasks as complete
- Delete tasks
- Access task data through a REST API
- Persist data using SQLite

## Project structure

- `main.py` — interactive CLI task manager
- `app.py` — FastAPI API endpoints
- `database.py` — database setup and CRUD logic
- `models.py` — Task model
- `tasks.db` — SQLite database created automatically when the app runs

## Requirements

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Run the CLI app

```bash
python main.py
```

The CLI presents a menu with these options:

1. Add task
2. View tasks
3. Complete task
4. Delete task
5. Exit

## Run the API server

```bash
uvicorn app:app --reload
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## API endpoints

### `GET /`
Returns a simple health message.

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

## Example usage

```bash
curl http://127.0.0.1:8000/tasks
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","priority":"medium"}'
```

## Notes

- The app creates the SQLite database automatically if it does not exist.
- For local development, the repository now includes a `requirements.txt` and project hygiene defaults for a cleaner production-readiness workflow.

## Testing

Run the test suite with:

```bash
pytest
