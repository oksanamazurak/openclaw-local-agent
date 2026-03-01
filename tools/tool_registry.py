from langchain_core.tools import tool
from tools.search import internet_search
from tools.todo_manager import add_todo, complete_todo, get_todos


@tool
def save_to_memory(text: str) -> str:
    """Save an important fact, preference, or piece of information to long-term memory.

    Use this when the user shares personal facts, preferences, or important
    information that should be remembered across conversations.
    """
    return f"Noted for long-term memory: {text}"


def get_all_tools() -> list:
    return [internet_search, add_todo, complete_todo, get_todos, save_to_memory]
