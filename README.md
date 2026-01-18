# CLI Task Manager (Python + SQLite)

A simple terminal-based task manager that stores tasks in a local SQLite 
database.

## Features
- Add tasks
- List tasks (pending or all)
- Mark tasks as done
- Delete tasks
- Persistent storage with SQLite

## Run

```bash
python3 -m task_manager add "My task"
python3 -m task_manager list
python3 -m task_manager done 1
python3 -m task_manager list --all
python3 -m task_manager delete 1

## Tech
- Python 3
- SQLite
- argparse
- Terminal-only interface

