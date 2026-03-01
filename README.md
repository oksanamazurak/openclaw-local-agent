# OpenClaw — Local AI Agent

A locally-running AI assistant built with LangGraph, Ollama, and Streamlit. No cloud API keys required.

## Requirements

- Python 3.12
- [Ollama](https://ollama.com/) running locally
- Pipenv (`pip install pipenv`)
- Docker (optional, for ChromaDB)

## Setup

**1. Install dependencies**

```bash
pipenv install
```

**2. Pull the Ollama model**

```bash
ollama pull qwen2.5:7b
```

**3. Start ChromaDB** (required for long-term memory)

```bash
docker run -p 8000:8000 chromadb/chroma:latest
```

**4. Run the app**

```bash
pipenv shell
streamlit run ui/main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Docker Compose (alternative)

Runs the agent and ChromaDB together. Ollama must still be running on the host.

```bash
docker compose up --build
```

## Switching models

Edit `DEFAULT_MODEL` in `backend/agent.py`:

```python
DEFAULT_MODEL = "llama3"  
```
