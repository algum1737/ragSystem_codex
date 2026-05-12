import logging
import numpy as np
from sentence_transformers import SentenceTransformer
from .chunker import Chunk

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "intfloat/multilingual-e5-large"

_E5_PREFIXES = ("intfloat/multilingual-e5", "intfloat/e5-")


def _needs_prefix(model_name: str) -> bool:
    return any(model_name.startswith(p) for p in _E5_PREFIXES)


class EmbeddingEngine:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        logger.info("임베딩 모델 로드 중: %s", model_name)
        try:
            self._model = SentenceTransformer(model_name)
        except Exception as e:
            raise RuntimeError(
                f"임베딩 모델 로드 실패: {model_name}. "
                f"모델이 캐시에 없으면 인터넷 연결 후 최초 1회 다운로드가 필요합니다. "
                f"(intfloat/multilingual-e5-large: 최초 실행 시 약 560MB 다운로드 필요)"
            ) from e
        self.model_name = model_name
        self._needs_prefix = _needs_prefix(model_name)
        logger.info("임베딩 모델 로드 완료: %s (dim=%d)", model_name, self._model.get_sentence_embedding_dimension())

    def embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self._model.get_sentence_embedding_dimension()))
        result = self._model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
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
        result = self._model.encode([text], show_progress_bar=False, convert_to_numpy=True)
        return result[0]
