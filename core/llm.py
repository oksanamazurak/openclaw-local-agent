import os
from langchain_ollama import ChatOllama

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = "qwen2.5:7b"


def build_llm(model_name: str = DEFAULT_MODEL, temperature: float = 0.2, num_ctx: int = 4096) -> ChatOllama:
    """Return a configured ChatOllama instance (without bound tools)."""
    return ChatOllama(
        model=model_name,
        base_url=OLLAMA_HOST,
        temperature=temperature,
        num_ctx=num_ctx,
    )
