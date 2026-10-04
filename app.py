from pathlib import Path
from typing import List, Literal

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import database
from settings import settings


app = FastAPI(title="Task Assistant API", version="1.9.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.cors_origins == ["*"] else settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def enforce_api_token(request: Request, call_next):
    if not settings.api_token:
        return await call_next(request)

    public_paths = {"/", "/api/", "/api/health", "/api/ready", "/health", "/ready"}
    if request.url.path in public_paths:
        return await call_next(request)

    if request.url.path.startswith("/static"):
        return await call_next(request)

    if request.url.path.startswith("/api") or request.url.path.startswith("/tasks"):
        auth_header = request.headers.get("Authorization", "")
        if auth_header != f"Bearer {settings.api_token}":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Unauthorized"},
            )

    return await call_next(request)


static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

database.initialize_database()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    priority: Literal["high", "medium", "low"]


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    priority: Literal["high", "medium", "low"]


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: Literal["high", "medium", "low"]
    completed: bool


class TaskMessageResponse(BaseModel):
    message: str


def _task_to_response(task):
    return {
        "id": task[0],
        "title": task[1],
        "priority": task[2],
        "completed": bool(task[3]),
    }


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(static_dir / "index.html")


@app.get("/api/", response_model=dict)
def home_api():
    return {"message": "Task Assistant API is running!"}


@app.get("/api/health")
def health_check_api():
    return {"status": "ok"}


@app.get("/api/ready")
def readiness_check_api():
    return {"status": "ready"}


@app.get("/api/tasks", response_model=List[TaskResponse])
def get_tasks_api():
    tasks = database.get_tasks()
    return [_task_to_response(task) for task in tasks]


@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_api(task: TaskCreate):
    task_id = database.create_task(task.title, task.priority)
    return {
        "id": task_id,
        "title": task.title,
        "priority": task.priority,
        "completed": False,
    }


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task_api(task_id: int):
    task = database.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return _task_to_response(task)


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task_api(task_id: int, task: TaskUpdate):
    updated = database.update_task(task_id, task.title, task.priority)
    if updated == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    saved_task = database.get_task(task_id)
    if saved_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return _task_to_response(saved_task)


@app.put("/api/tasks/{task_id}/complete", response_model=TaskMessageResponse)
def complete_task_api(task_id: int):
    updated = database.complete_task(task_id)
    if updated == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task completed successfully"}


@app.delete("/api/tasks/{task_id}", response_model=TaskMessageResponse)
def delete_task_api(task_id: int):
    deleted = database.delete_task(task_id)
    if deleted == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task deleted successfully"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready"}


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    tasks = database.get_tasks()
    return [_task_to_response(task) for task in tasks]


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    task_id = database.create_task(task.title, task.priority)
    return {
        "id": task_id,
        "title": task.title,
        "priority": task.priority,
        "completed": False,
    }


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = database.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return _task_to_response(task)


@app.put("/tasks/{task_id}/complete", response_model=TaskMessageResponse)
def complete_task(task_id: int):
    updated = database.complete_task(task_id)
    if updated == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task completed successfully"}


@app.delete("/tasks/{task_id}", response_model=TaskMessageResponse)
def delete_task(task_id: int):
    deleted = database.delete_task(task_id)
    if deleted == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task deleted successfully"}
