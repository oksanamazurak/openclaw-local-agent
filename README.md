# OpenClaw — Local AI Agent

A locally-running AI assistant built with LangGraph, Ollama, and Streamlit. No cloud API keys required.

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
