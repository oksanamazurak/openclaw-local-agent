import json
from pathlib import Path
from langchain_core.tools import tool

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
TODOS_FILE = _PROJECT_ROOT / "data" / "todos.json"


def _read_todos() -> list[dict]:
    if not TODOS_FILE.exists():
        return []
    try:
        with open(TODOS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _write_todos(todos: list[dict]) -> None:
    TODOS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TODOS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)


def _next_id(todos: list[dict]) -> int:
    if not todos:
        return 1
    return max(t.get("id", 0) for t in todos) + 1


@tool
def add_todo(task: str) -> str:
    """Add a new task to the to-do list."""
    todos = _read_todos()
    new_id = _next_id(todos)
    todos.append({"id": new_id, "task": task, "done": False})
    _write_todos(todos)
    return f"Added task #{new_id}: {task}"


@tool
def complete_todo(task_id: int) -> str:
    """Mark a to-do task as completed."""
    todos = _read_todos()
    for t in todos:
        if t.get("id") == task_id:
            t["done"] = True
            _write_todos(todos)
            return f"Task #{task_id} marked as done: {t['task']}"
    return f"Task #{task_id} not found."


@tool
def get_todos() -> str:
    """Get the current to-do list with all tasks and their statuses."""
    todos = _read_todos()
    if not todos:
        return "The to-do list is empty."
    lines = []
    for t in todos:
        status = "✅ Done" if t.get("done") else "⬜ Pending"
        lines.append(f"#{t['id']}: {t['task']} [{status}]")
    return "\n".join(lines)


def load_todos_for_ui() -> list[dict]:
    """Load the to-do list for display in the Streamlit UI."""
    return _read_todos()


def mark_todo_done(task_id: int) -> None:
    """Mark a task as done directly (UI helper)."""
    todos = _read_todos()
    for t in todos:
        if t.get("id") == task_id:
            t["done"] = True
            break
    _write_todos(todos)
