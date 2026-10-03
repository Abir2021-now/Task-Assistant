from fastapi import FastAPI
import database


app = FastAPI()

database.initialize_database()


@app.get("/")
def home():
    return {"message": "Task Assistant API is running!"}


@app.get("/tasks")
def get_tasks():
    tasks = database.get_tasks()
    return tasks
