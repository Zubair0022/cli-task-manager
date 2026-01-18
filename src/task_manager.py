import argparse
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tasks.db"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    return conn


def add_task(title: str):
    with connect() as conn:
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    print(f"Added: {title}")


def list_tasks(show_all: bool):
    query = "SELECT id, title, done, created_at FROM tasks"
    if not show_all:
        query += " WHERE done = 0"
    query += " ORDER BY id DESC"

    with connect() as conn:
        rows = conn.execute(query).fetchall()

    if not rows:
        print("No tasks found.")
        return

    for task_id, title, done, created_at in rows:
        status = "✓" if done else " "
        print(f"[{status}] {task_id}: {title}  (created: {created_at})")


def done_task(task_id: int):
    with connect() as conn:
        cur = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            print("Task not found.")
            return
    print(f"Marked done: {task_id}")


def delete_task(task_id: int):
    with connect() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            print("Task not found.")
            return
    print(f"Deleted: {task_id}")


def main():
    parser = argparse.ArgumentParser(prog="task", description="Simple CLI Task Manager (SQLite)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--all", action="store_true", help="Show completed tasks too")

    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="Task ID")

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.cmd == "add":
        add_task(args.title)
    elif args.cmd == "list":
        list_tasks(args.all)
    elif args.cmd == "done":
        done_task(args.id)
    elif args.cmd == "delete":
        delete_task(args.id)


if __name__ == "__main__":
    main()
