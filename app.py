import logging
import os
import sqlite3
from typing import List, Literal

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import database


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("task_assistant")

app = FastAPI(title="Task Assistant API", version="1.2.0")

allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")
allowed_origins = [origin.strip() for origin in allowed_origins if origin.strip()]
if not allowed_origins:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allowed_origins == ["*"] else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Request started: %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        logger.info(
            "Request finished: %s %s -> %s",
            request.method,
            request.url.path,
            response.status_code,
        )
        return response
    except Exception:
        logger.exception("Request failed: %s %s", request.method, request.url.path)
        raise


@app.exception_handler(ValueError)
async def value_error_handler(_, exc: ValueError):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.exception_handler(sqlite3.DatabaseError)
async def database_error_handler(_, exc: sqlite3.DatabaseError):
    logger.exception("Database error encountered: %s", exc)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database error",
    )


database.initialize_database()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    priority: Literal["high", "medium", "low"]


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: Literal["high", "medium", "low"]
    completed: bool


class TaskMessageResponse(BaseModel):
    message: str


@app.get("/", response_model=dict)
def home():
    return {"message": "Task Assistant API is running!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready"}


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    tasks = database.get_tasks()
    return [
        {
            "id": task[0],
            "title": task[1],
            "priority": task[2],
            "completed": bool(task[3]),
        }
        for task in tasks
    ]


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return {
        "id": task[0],
        "title": task[1],
        "priority": task[2],
        "completed": bool(task[3]),
    }


@app.put("/tasks/{task_id}/complete", response_model=TaskMessageResponse)
def complete_task(task_id: int):
    updated = database.complete_task(task_id)

    if updated == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return {"message": "Task completed successfully"}


@app.delete("/tasks/{task_id}", response_model=TaskMessageResponse)
def delete_task(task_id: int):
    deleted = database.delete_task(task_id)

    if deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return {"message": "Task deleted successfully"}
