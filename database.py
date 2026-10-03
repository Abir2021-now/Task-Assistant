import sqlite3


DATABASE_NAME = "tasks.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            completed INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def create_task(title, priority):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, priority, completed)
        VALUES (?, ?, ?)
    """, (title, priority, 0))

    connection.commit()
    connection.close()

def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, priority, completed
        FROM tasks
    """)

    tasks = cursor.fetchall()

    connection.close()

    return tasks

def complete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
    """, (task_id,))

    updated = cursor.rowcount

    connection.commit()
    connection.close()

    return updated


def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted

