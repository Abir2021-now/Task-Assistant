from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import database


app = FastAPI()

database.initialize_database()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    priority: Literal["high", "medium", "low"]


@app.get("/")
def home():
    return {"message": "Task Assistant API is running!"}


@app.get("/tasks")
def get_tasks():
    tasks = database.get_tasks()
    return tasks

@app.post("/tasks")
def create_task(task: TaskCreate):
    task_id = database.create_task(
        task.title,
        task.priority
    )

    return {
        "id": task_id,
        "title": task.title,
        "priority": task.priority,
        "completed": False
    }

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = database.get_task(task_id)

    if task is None:
        return {"error": "Task not found"}

    return {
        "id": task[0],
        "title": task[1],
        "priority": task[2],
        "completed": bool(task[3])
    }
