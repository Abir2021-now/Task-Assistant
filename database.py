import os
from typing import Optional

from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import settings


DATABASE_URL = os.getenv("DATABASE_URL", settings.database_url)

Base = declarative_base()


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    priority = Column(String(20), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)


connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialize_database():
    Base.metadata.create_all(bind=engine)


def _validate_title(title: str) -> str:
    if not isinstance(title, str):
        raise ValueError("Task title must be a string.")

    cleaned_title = title.strip()
    if not cleaned_title:
        raise ValueError("Task title cannot be empty.")

    return cleaned_title


def _validate_priority(priority: str) -> str:
    valid_priorities = {"high", "medium", "low"}
    if priority not in valid_priorities:
        raise ValueError("Priority must be one of: high, medium, low.")
    return priority


def create_task(title: str, priority: str) -> int:
    cleaned_title = _validate_title(title)
    cleaned_priority = _validate_priority(priority)

    session = SessionLocal()
    try:
        task = TaskORM(title=cleaned_title, priority=cleaned_priority, completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.id
    finally:
        session.close()


def get_tasks() -> list[tuple[int, str, str, int]]:
    session = SessionLocal()
    try:
        tasks = session.query(TaskORM).order_by(TaskORM.id).all()
        return [(task.id, task.title, task.priority, int(task.completed)) for task in tasks]
    finally:
        session.close()


def get_task(task_id: int) -> Optional[tuple[int, str, str, int]]:
    session = SessionLocal()
    try:
        task = session.query(TaskORM).filter(TaskORM.id == task_id).first()
        if task is None:
            return None
        return (task.id, task.title, task.priority, int(task.completed))
    finally:
        session.close()


def complete_task(task_id: int) -> int:
    session = SessionLocal()
    try:
        task = session.query(TaskORM).filter(TaskORM.id == task_id).first()
        if task is None:
            return 0
        task.completed = True
        session.commit()
        return 1
    finally:
        session.close()


def delete_task(task_id: int) -> int:
    session = SessionLocal()
    try:
        task = session.query(TaskORM).filter(TaskORM.id == task_id).first()
        if task is None:
            return 0
        session.delete(task)
        session.commit()
        return 1
    finally:
        session.close()
