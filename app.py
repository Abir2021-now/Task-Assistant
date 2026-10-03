from fastapi import FastAPI
from pydantic import BaseModel

import database


app = FastAPI()

database.initialize_database()


class TaskCreate(BaseModel):
    title: str
    priority: str


@app.get("/")
def home():
    return {"message": "Task Assistant API is running!"}


@app.get("/tasks")
def get_tasks():
    tasks = database.get_tasks()
    return tasks
    
@app.post("/tasks")
def create_task(task: TaskCreate):
    database.create_task(
        task.title,
        task.priority
    )
    return {
        "message": "Task created successfully"
    }
