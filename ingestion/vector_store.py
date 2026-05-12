import logging
from pathlib import Path

import chromadb
import numpy as np

from .chunker import Chunk

logger = logging.getLogger(__name__)

DEFAULT_COLLECTION = "ragSystem"
DEFAULT_DB_PATH = "./chroma_db"


class VectorStore:
    def __init__(self, db_path: str = DEFAULT_DB_PATH, collection_name: str = DEFAULT_COLLECTION):
        self._client = chromadb.PersistentClient(path=db_path)
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.collection_name = collection_name
        logger.info("VectorStore 초기화: collection=%s, db=%s", collection_name, db_path)

    def add_chunks(self, chunks: list[Chunk], embeddings: list[np.ndarray]) -> int:
        if not chunks:
            return 0
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"chunks({len(chunks)})와 embeddings({len(embeddings)}) 수가 일치하지 않습니다"
            )
        ids = [f"{c.source_path}::{c.chunk_index}" for c in chunks]
        documents = [c.text for c in chunks]
        metadatas = [{**c.metadata, "source_path": c.source_path} for c in chunks]
        vectors = [e.tolist() for e in embeddings]
        self._collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas,
        )
        logger.info("upsert 완료: %d개 청크 → collection=%s", len(chunks), self.collection_name)
        return len(chunks)

    def similarity_search(self, query_embedding: np.ndarray, k: int = 5, where: dict | None = None) -> list[dict]:
        count = self._collection.count()
        if count == 0:
            return []
        n_results = min(k, count)
        query_kwargs: dict = {
            "query_embeddings": [query_embedding.tolist()],
            "n_results": n_results,
        }
        if where:
            query_kwargs["where"] = where
        try:
            results = self._collection.query(**query_kwargs)
        except Exception:
            try:
                query_kwargs["n_results"] = 1
                results = self._collection.query(**query_kwargs)
            except Exception:
                return []
        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "text": results["documents"][0][i],
                "source_path": results["metadatas"][0][i].get("source_path", ""),
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })
        return output

    def get_stats(self) -> dict:
        return {"count": self._collection.count(), "collection_name": self.collection_name}

    def reset(self) -> None:
        self._client.delete_collection(self.collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("컬렉션 초기화 완료: %s", self.collection_name)
