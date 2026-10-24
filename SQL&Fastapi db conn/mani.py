
from fastapi import FastAPI
import sqlite3

app = FastAPI()


def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_table()


@app.get("/")
def home():
    return {"message": "Task Manager API"}


@app.post("/tasks")
def create_task(task: str):
    conn = get_db()

    cursor = conn.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (task,)
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {"id": task_id, "task": task}


@app.get("/tasks")
def get_tasks():
    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return {"tasks": [dict(row) for row in rows]}
  
