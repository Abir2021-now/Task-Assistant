from fastapi.testclient import TestClient

import app


client = TestClient(app.app)


def test_home_endpoint():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Assistant API is running!"}


def test_create_task_and_get_tasks(monkeypatch, tmp_path):
    db_path = tmp_path / "tasks.db"
    monkeypatch.setattr(app.database, "DATABASE_NAME", str(db_path))
    app.database.initialize_database()

    payload = {"title": "Write docs", "priority": "high"}
    create_response = client.post("/api/tasks", json=payload)

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == payload["title"]
    assert created["priority"] == payload["priority"]
    assert created["completed"] is False

    list_response = client.get("/api/tasks")
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Write docs"


def test_get_missing_task_returns_404():
    response = client.get("/api/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_complete_task_marks_task_done(monkeypatch, tmp_path):
    db_path = tmp_path / "tasks.db"
    monkeypatch.setattr(app.database, "DATABASE_NAME", str(db_path))
    app.database.initialize_database()

    client.post("/api/tasks", json={"title": "Ship feature", "priority": "medium"})
    response = client.put("/api/tasks/1/complete")

    assert response.status_code == 200
    assert response.json() == {"message": "Task completed successfully"}

    task_response = client.get("/api/tasks/1")
    assert task_response.status_code == 200
    assert task_response.json()["completed"] is True
