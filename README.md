# OpenClaw — Local AI Agent

A locally-running AI assistant built with LangGraph, Ollama, and Streamlit. No cloud API keys required.

## Features

- 🤖 Conversational agent powered by a local Ollama model
- 🧠 Short-term and long-term (ChromaDB) memory
- 🔧 Built-in tools: internet search, to-do manager, memory saving
- 🔍 "Under the Hood" debug page showing the agent's reasoning steps
- 🐳 Docker Compose for easy one-command setup

## Project Structure

```
openclaw-local-agent/
├── app.py               # Streamlit entry point
├── core/
│   ├── agent.py         # LangGraph agent, graph construction & caching
│   ├── llm.py           # Ollama LLM setup (DEFAULT_MODEL lives here)
│   └── prompts.py       # System and proactive prompts
├── memory/
│   ├── short_term.py    # In-session message history
│   └── long_term.py     # ChromaDB-backed persistent memory
├── tools/
│   ├── search.py        # Internet search via ddgs
│   ├── todo_manager.py  # To-do list CRUD
│   └── tool_registry.py # Tool registration for the agent
├── ui/
│   ├── page_agent.py    # Agent chat interface
│   ├── page_debug.py    # Debug / monologue view
│   ├── session.py       # Streamlit session state helpers
│   └── components/      # Sidebar and other UI components
├── data/                # Persistent data (todos.json, etc.)
├── Dockerfile
└── docker-compose.yml
```

## Requirements

- Python 3.12
- [Ollama](https://ollama.com/) running locally
- Pipenv (`pip install pipenv`)
- Docker (required for ChromaDB)

## Setup

**1. Install dependencies**

```bash
pipenv install
```

**2. Pull the Ollama model**

```bash
ollama pull qwen2.5:7b
```

**3. Start ChromaDB and run the app via Docker Compose**

```bash
docker compose up --build
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

> Ollama must still be running on the host machine. The agent container connects to it automatically via `host.docker.internal`.

## Running Without Docker

If you prefer to run without Docker, start ChromaDB separately first:

```bash
docker run -p 8000:8000 chromadb/chroma:latest
```

Then run the app:

```bash
pipenv shell
streamlit run app.py
```

## Switching Models

Edit `DEFAULT_MODEL` in `core/llm.py`:

```python
DEFAULT_MODEL = "qwen2.5:7b"
```

Then restart the app. The compiled agent graph is cached per model name and rebuilt automatically when the model changes.
