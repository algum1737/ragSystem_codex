import logging
import os
from typing import Any
import numpy as np
from .chunker import Chunk

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "intfloat/multilingual-e5-large"

_E5_PREFIXES = ("intfloat/multilingual-e5", "intfloat/e5-")


def _needs_prefix(model_name: str) -> bool:
    return any(model_name.startswith(p) for p in _E5_PREFIXES)


class EmbeddingEngine:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self._needs_prefix = _needs_prefix(model_name)
        self._model: Any | None = None

    def _ensure_model(self) -> Any:
        if self._model is not None:
            return self._model
        logger.info("임베딩 모델 로드 중: %s", self.model_name)
        original_hf_offline = os.environ.get("HF_HUB_OFFLINE")
        original_transformers_offline = os.environ.get("TRANSFORMERS_OFFLINE")
        try:
            # Prefer fully offline loading first when the cache is already present.
            os.environ["HF_HUB_OFFLINE"] = "1"
            os.environ["TRANSFORMERS_OFFLINE"] = "1"
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name, local_files_only=True)
        except Exception as e:
            try:
                if original_hf_offline is None:
                    os.environ.pop("HF_HUB_OFFLINE", None)
                else:
                    os.environ["HF_HUB_OFFLINE"] = original_hf_offline
                if original_transformers_offline is None:
                    os.environ.pop("TRANSFORMERS_OFFLINE", None)
                else:
                    os.environ["TRANSFORMERS_OFFLINE"] = original_transformers_offline
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except Exception as inner:
                raise RuntimeError(
                    f"임베딩 모델 로드 실패: {self.model_name}. "
                    f"모델이 캐시에 없으면 인터넷 연결 후 최초 1회 다운로드가 필요합니다. "
                    f"(intfloat/multilingual-e5-large: 최초 실행 시 약 560MB 다운로드 필요)"
                ) from inner
        finally:
            if original_hf_offline is None:
                os.environ.pop("HF_HUB_OFFLINE", None)
            else:
                os.environ["HF_HUB_OFFLINE"] = original_hf_offline
            if original_transformers_offline is None:
                os.environ.pop("TRANSFORMERS_OFFLINE", None)
            else:
                os.environ["TRANSFORMERS_OFFLINE"] = original_transformers_offline
        logger.info(
            "임베딩 모델 로드 완료: %s (dim=%d)",
            self.model_name,
            self._model.get_sentence_embedding_dimension(),
        )
        return self._model

    def embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 0))
        model = self._ensure_model()
        result = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        logger.debug("임베딩 완료: %d개 텍스트, shape=%s, 모델=%s", len(texts), result.shape, self.model_name)
        return result

    def embed_chunks(self, chunks: list[Chunk]) -> list[np.ndarray]:
        if not chunks:
            return []
        texts = [f"passage: {c.text}" if self._needs_prefix else c.text for c in chunks]
        embeddings = self.embed(texts)
        return list(embeddings)

    def embed_query(self, question: str) -> np.ndarray:
        if not question.strip():
            raise ValueError("question이 비어 있습니다")
        text = f"query: {question}" if self._needs_prefix else question
        model = self._ensure_model()
        result = model.encode([text], show_progress_bar=False, convert_to_numpy=True)
        return result[0]
