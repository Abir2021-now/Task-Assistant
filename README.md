# Task Assistant

Task Assistant is a Python-based task manager that stores tasks in a SQLite database. The project includes both a command-line interface (CLI) and a FastAPI REST API, making it useful for simple local task tracking and lightweight API-based task management.

## Features

- Add a task with a title and priority (`high`, `medium`, or `low`)
- View all saved tasks
- Mark tasks as complete
- Delete tasks
- Access tasks through a REST API
- Persistent storage using SQLite

## Project structure

- `main.py` — CLI-based task manager interface
- `app.py` — FastAPI API endpoints
- `database.py` — SQLite database setup and CRUD operations
- `models.py` — simple `Task` model
- `tasks.db` — SQLite database created automatically when the project runs

## Requirements

Install the Python dependencies needed for the API:

```bash
pip install fastapi uvicorn pydantic
```

## Run the CLI app

```bash
python main.py
```

This opens a menu where you can:

1. Add a task
2. View tasks
3. Complete a task
4. Delete a task
5. Exit

## Run the API server

```bash
uvicorn app:app --reload
```

Then open:

- `http://127.0.0.1:8000/`

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
Returns a specific task by its ID.

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

The app creates the SQLite database automatically on startup. If the database file does not exist yet, it will be generated when the app is run.