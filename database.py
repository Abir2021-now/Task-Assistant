import os
import sqlite3


DATABASE_NAME = os.getenv("DATABASE_NAME", "tasks.db")


def get_connection():
    return sqlite3.connect(DATABASE_NAME, timeout=30)


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
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Task title cannot be empty.")

    valid_priorities = {"high", "medium", "low"}
    if priority not in valid_priorities:
        raise ValueError("Priority must be one of: high, medium, low.")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, priority, completed)
        VALUES (?, ?, ?)
        """,
        (title.strip(), priority, 0),
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
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, priority, completed
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )

    task = cursor.fetchone()
    connection.close()
    return task


def complete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
        """,
        (task_id,),
    )

    updated = cursor.rowcount
    connection.commit()
    connection.close()
    return updated


def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )

    deleted = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted
