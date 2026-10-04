import os
import sqlite3


DATABASE_NAME = os.getenv("DATABASE_NAME", "tasks.db")


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def _validate_title(title):
    if not isinstance(title, str):
        raise ValueError("Task title must be a string.")

    cleaned_title = title.strip()
    if not cleaned_title:
        raise ValueError("Task title cannot be empty.")

    return cleaned_title


def _validate_priority(priority):
    valid_priorities = {"high", "medium", "low"}
    if priority not in valid_priorities:
        raise ValueError("Priority must be one of: high, medium, low.")
    return priority


def _validate_task_id(task_id):
    try:
        task_id_int = int(task_id)
    except (TypeError, ValueError):
        raise ValueError("Task ID must be a valid integer.")

    if task_id_int <= 0:
        raise ValueError("Task ID must be greater than zero.")

    return task_id_int


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            completed INTEGER NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def create_task(title, priority):
    cleaned_title = _validate_title(title)
    cleaned_priority = _validate_priority(priority)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, priority, completed)
        VALUES (?, ?, ?)
        """,
        (cleaned_title, cleaned_priority, 0),
    )

    task_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return task_id


def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, priority, completed
        FROM tasks
        ORDER BY id
        """
    )

    tasks = cursor.fetchall()
    connection.close()
    return tasks


def get_task(task_id):
    validated_task_id = _validate_task_id(task_id)
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, priority, completed
        FROM tasks
        WHERE id = ?
        """,
        (validated_task_id,),
    )

    task = cursor.fetchone()
    connection.close()
    return task


def complete_task(task_id):
    validated_task_id = _validate_task_id(task_id)
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
        """,
        (validated_task_id,),
    )

    updated = cursor.rowcount
    connection.commit()
    connection.close()
    return updated


def delete_task(task_id):
    validated_task_id = _validate_task_id(task_id)
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (validated_task_id,),
    )

    deleted = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted
