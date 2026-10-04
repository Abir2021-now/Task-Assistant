import logging
import os
import time
from collections import defaultdict, deque
from typing import Deque, Dict, List, Literal

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import database
from settings import settings


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("task_assistant")

API_TOKEN = os.getenv("API_TOKEN")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "60"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

app = FastAPI(title="Task Assistant API", version="1.6.0")

database.DATABASE_URL = settings.database_url

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.cors_origins == ["*"] else settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

request_times: Dict[str, Deque[float]] = defaultdict(deque)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = request_times[client_ip]
    window.append(now)

    while window and now - window[0] > RATE_LIMIT_WINDOW_SECONDS:
        window.popleft()

    if len(window) > RATE_LIMIT:
        logger.warning("Rate limit exceeded for %s", client_ip)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )

    if API_TOKEN:
        auth_header = request.headers.get("Authorization", "")
        expected = f"Bearer {API_TOKEN}"
        if auth_header != expected:
            logger.warning("Unauthorized request from %s", client_ip)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

    logger.info("Request started: %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("Request finished: %s %s -> %s", request.method, request.url.path, response.status_code)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task completed successfully"}


@app.delete("/tasks/{task_id}", response_model=TaskMessageResponse)
def delete_task(task_id: int):
    deleted = database.delete_task(task_id)
    if deleted == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task deleted successfully"}
