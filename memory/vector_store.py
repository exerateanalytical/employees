"""
Vector memory store — ChromaDB, fully local, fully offline.
One collection per agent. Persists to disk between sessions.
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

import chromadb

MEMORY_DIR = Path(__file__).parent.parent / "memory_store"
MEMORY_DIR.mkdir(exist_ok=True)

_client: chromadb.PersistentClient | None = None


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(MEMORY_DIR))
    return _client


class VectorStore:
    """
    Semantic memory store for one agent.
    Stores text + metadata. Retrieves by meaning, not exact keyword.
    """

    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name.lower()
        self.collection = _get_client().get_or_create_collection(
            name=f"opes_{self.agent_name}",
            metadata={"hnsw:space": "cosine"},
        )

    def store(
        self,
        text: str,
        memory_type: str,
        metadata: dict[str, Any] | None = None,
        memory_id: str | None = None,
    ) -> str:
        mid = memory_id or str(uuid.uuid4())
        meta = {"memory_type": memory_type, "agent": self.agent_name}
        if metadata:
            meta.update(metadata)
        # ChromaDB requires all metadata values to be str/int/float/bool
        meta = {k: str(v) for k, v in meta.items()}
        self.collection.add(documents=[text], metadatas=[meta], ids=[mid])
        return mid

    def retrieve(self, query: str, n: int = 5, memory_type: str | None = None) -> list[dict]:
        where = {"memory_type": memory_type} if memory_type else None
        kwargs: dict[str, Any] = {"query_texts": [query], "n_results": min(n, self.count() or 1)}
        if where:
            kwargs["where"] = where
        results = self.collection.query(**kwargs)
        if not results["documents"] or not results["documents"][0]:
            return []
        return [
            {"text": doc, "metadata": meta, "relevance": round(1 - dist, 3)}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def get_recent(self, n: int = 10, memory_type: str | None = None) -> list[dict]:
        where = {"memory_type": memory_type} if memory_type else None
        kwargs: dict[str, Any] = {"limit": n, "include": ["documents", "metadatas"]}
        if where:
            kwargs["where"] = where
        results = self.collection.get(**kwargs)
        if not results["documents"]:
            return []
        return [
            {"text": doc, "metadata": meta}
            for doc, meta in zip(results["documents"], results["metadatas"])
        ]

    def count(self) -> int:
        return self.collection.count()

    def delete(self, memory_id: str) -> None:
        self.collection.delete(ids=[memory_id])

    def stats(self) -> dict:
        return {"agent": self.agent_name, "total_memories": self.count()}
