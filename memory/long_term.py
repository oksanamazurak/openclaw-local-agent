import os
import uuid
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

CHROMA_HOST = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8000"))
COLLECTION_NAME = "agent_memory"


class LongTermMemory:
    """ChromaDB-backed vector memory."""

    def __init__(self):
        self._client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        self._ef = DefaultEmbeddingFunction()
        self._collection = self._client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self._ef,
        )

    def store(self, text: str, metadata: dict | None = None) -> str:
        doc_id = str(uuid.uuid4())
        self._collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[metadata or {}],
        )
        return doc_id

    def search(self, query: str, k: int = 3) -> list[dict]:
        results = self._collection.query(query_texts=[query], n_results=k)
        docs = []
        if results and results.get("documents"):
            for i, doc in enumerate(results["documents"][0]):
                docs.append({
                    "document": doc,
                    "id": results["ids"][0][i] if results.get("ids") else None,
                    "distance": results["distances"][0][i] if results.get("distances") else None,
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else None,
                })
        return docs

    def get_all(self) -> list[dict]:
        try:
            data = self._collection.get()
            if not data or not data.get("documents"):
                return []
            return [
                {
                    "id": data["ids"][i],
                    "document": doc,
                    "metadata": data["metadatas"][i] if data.get("metadatas") else {},
                }
                for i, doc in enumerate(data["documents"])
            ]
        except Exception:
            return []

    def count(self) -> int:
        try:
            return self._collection.count()
        except Exception:
            return 0
