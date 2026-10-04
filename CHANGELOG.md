# Task Assistant

Task Assistant is a Python-based task manager for creating, listing, completing, and deleting tasks. The project includes a command-line interface and a lightweight FastAPI API backed by SQLite.

## Features

- Create tasks with a title and priority
- View all saved tasks
- Mark tasks as complete
- Delete tasks
- Query the API over HTTP
- Store data persistently in SQLite

```markdown
## Unreleased

- Step 2: Added automated tests and a GitHub Actions CI workflow for the project.
- Step 1: Added dependency management (`requirements.txt`), `.gitignore`, and `LICENSE`.
- Step 1: Fixed the missing `database.get_tasks()` bug and hardened CLI ID validation.

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
└── tasks.db
```

## Requirements

```bash
pip install -r requirements.txt
```

## Run the CLI

```bash
python main.py
```

## Run the API

```bash
uvicorn app:app --reload
```

Then visit:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs

## Example API request

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Plan sprint work","priority":"high"}'
```

## Notes

- The database file is created automatically when the app is started.
- This repository is in active production-readiness setup and is being hardened step by step.
