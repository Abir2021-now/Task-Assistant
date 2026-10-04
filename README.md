# Task Assistant

Task Assistant is a Python-based task manager with a FastAPI backend and a lightweight browser UI.

## Features

- Create tasks with title and priority
- View all tasks
- Mark tasks complete
- Delete tasks
- Use the API directly or through the browser UI
- Store data in SQLite by default
- Run locally or in Docker

## Project structure

```text
.
├── app.py
├── database.py
├── settings.py
├── static/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── main.py
├── README.md
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── tests/
│   └── test_app.py
├── tasks.db
└── __pycache__/
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- `http://127.0.0.1:8000/` for the browser UI
- `http://127.0.0.1:8000/docs` for the API docs
- `http://127.0.0.1:8000/api/tasks` for raw task data

## Run with Docker

```bash
docker build -t task-assistant .
docker run -p 8000:8000 task-assistant
```

## API endpoints

- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/{task_id}`
- `PUT /api/tasks/{task_id}/complete`
- `DELETE /api/tasks/{task_id}`

## Configuration

```bash
DATABASE_NAME=tasks.db
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

## Testing

```bash
pytest
```
