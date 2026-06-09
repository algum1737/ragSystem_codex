import logging
import re
import threading
import time

from ingestion.embedder import EmbeddingEngine
from ingestion.vector_store import VectorStore
from observability.trace import is_trace_enabled, new_trace_id, trace_event
from .llm import OllamaLLM

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """당신은 주어진 참고 문서를 바탕으로 질문에 답변하는 지식 어시스턴트입니다.

답변 규칙:
1. 반드시 한국어로 답변하세요.
2. 참고 문서의 내용만 근거로 사용하세요. 문서에 없는 내용은 추측하지 마세요. "가능성", "것으로 보아"처럼 문서 밖 추론을 암시하는 표현도 쓰지 마세요.
3. 질문에 여러 하위 항목이 있으면 하위 항목별로 판단하세요.
   - 문서에서 확인되는 항목은 "확인된 내용"으로 답하세요.
   - 문서에서 확인되지 않는 항목은 "문서에서 확인되지 않는 내용"으로 분리해 밝히세요.
   - 예: A와 B를 물었는데 B만 확인되면 B는 답하고 A는 확인되지 않는다고 쓰세요.
4. 모든 하위 항목에 대한 답을 찾을 수 없을 때만 "제공된 문서에서 해당 정보를 찾을 수 없습니다."라고 답하세요.
5. 답변에 관련 내용이 있는 출처(문서명)를 함께 언급하세요.
6. 구체적이고 완결된 문장으로 답변하세요.

[참고 문서]
{context}

[질문]
{question}

[답변]"""

CONCISE_PROMPT_TEMPLATE = """당신은 주어진 참고 문서만 근거로 답변하는 한국어 지식 어시스턴트입니다.

답변 규칙:
1. 반드시 한국어로 답변하세요.
2. 참고 문서에 있는 내용만 사용하고 추측하지 마세요.
3. 첫 줄부터 질문에 직접 답하는 핵심만 3~4개 bullet로 작성하세요.
4. 각 bullet은 1문장으로 제한하세요.
5. 같은 의미의 조건이나 서비스별 유사 처리는 하나의 bullet로 합치세요.
6. 질문과 직접 관련 없는 비용, 광고, 일반 안내, 배경 설명은 참고 문서에 있어도 제외하세요.
7. "문서에서 확인되지 않습니다", "확인되지 않은 항목" 같은 미확인 문장은 쓰지 마세요.
8. 마지막 줄에 "근거: 문서명1, 문서명2" 형식으로 가장 중요한 출처명을 최대 3개만 적으세요.
9. 근거에는 참고 문서의 "출처:" 뒤에 있는 실제 문서명만 그대로 쓰고, "문서1", "문서2", "[1]" 같은 번호 별칭은 쓰지 마세요.
10. 원문을 길게 인용하거나 같은 내용을 반복하지 마세요.

[참고 문서]
{context}

[질문]
{question}

[답변]"""

ANSWER_MODE_PROMPTS = {
    "standard": PROMPT_TEMPLATE,
    "concise": CONCISE_PROMPT_TEMPLATE,
}

NO_RESULTS_ANSWER = "인제스천된 문서가 없습니다. 먼저 인제스천 탭에서 문서를 업로드하세요."


def _elapsed_ms(start: float) -> float:
    return (time.perf_counter() - start) * 1000


def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[가-힣]+|[a-zA-Z0-9]+", text.lower())
    return tokens if tokens else [""]


_DOC_TYPE_ALIASES = {
    "일반": ["일반", "일반약관"],
    "위치기반서비스": ["위치기반서비스", "위치기반약관"],
}


def _doc_type_where(doc_type: str | None) -> dict | None:
    if not doc_type:
        return None
    values = _DOC_TYPE_ALIASES.get(doc_type, [doc_type])
    return {"doc_type": values[0]} if len(values) == 1 else {"doc_type": {"$in": values}}


def _metadata_matches(metadata: dict, where: dict | None) -> bool:
    if not where:
        return True
    for key, expected in where.items():
        actual = metadata.get(key)
        if isinstance(expected, dict) and "$in" in expected:
            if actual not in expected["$in"]:
                return False
        elif actual != expected:
            return False
    return True


class _BM25Cache:
    def __init__(self):
        self._index = None
        self._count = -1
        self._texts: list[str] = []
        self._docs: list[dict] = []

    def search(self, vs: VectorStore, query: str, n: int, where: dict | None = None) -> list[tuple[str, float]]:
        try:
            from rank_bm25 import BM25Okapi
        except ImportError:
            return []
        try:
            current_count = vs.get_stats()["count"]
            if current_count != self._count or not self._texts:
                raw = vs._collection.get()
                texts = raw.get("documents") or []
                metadatas = raw.get("metadatas") or []
                if not texts:
                    return []
                self._index = BM25Okapi([_tokenize(t) for t in texts])
                self._count = current_count
                self._texts = texts
                self._docs = [
                    {
                        "text": texts[i],
                        "source_path": (metadatas[i] or {}).get("source_path", "") if metadatas else "",
                        "metadata": metadatas[i] if metadatas else {},
                        "distance": 0.0,
                    }
                    for i in range(len(texts))
                ]
            if not self._texts:
                return []
            scores = self._index.get_scores(_tokenize(query))
            top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            if where:
                top_idx = [
                    i for i in top_idx
                    if _metadata_matches(self._docs[i].get("metadata", {}), where)
                ]
            top_idx = top_idx[:n]
            return [(self._texts[i], float(scores[i])) for i in top_idx]
        except Exception as e:
            logger.warning("BM25 검색 실패 (폴백): %s", e)
            return []

    def get_doc(self, text: str) -> dict | None:
        for doc in self._docs:
            if doc["text"] == text:
                return doc
        return None


_bm25_cache = _BM25Cache()

DEFAULT_RERANKER_MODEL = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"


class _CrossEncoderReranker:
    def __init__(self, model_name: str):
        self._model_name = model_name
        self._model = None
        self._lock = threading.Lock()

    def _load(self):
        if self._model is not None:
            return
        with self._lock:
            if self._model is not None:
                return
            try:
                from sentence_transformers import CrossEncoder
                self._model = CrossEncoder(self._model_name)
                logger.info("CrossEncoder 로드 완료: %s", self._model_name)
            except Exception as e:
                logger.warning("Cross-Encoder 로드 실패 (폴백): %s", e)
                self._model = False

    def rerank(self, question: str, texts: list[str], top_k: int) -> list[str]:
        if not texts:
            return []
        self._load()
        if not self._model:
            return texts[:top_k]
        try:
            pairs = [(question, t) for t in texts]
            scores = self._model.predict(pairs)
            ranked = sorted(zip(texts, scores), key=lambda x: x[1], reverse=True)
            selected = [t for t, _ in ranked[:top_k]]
            logger.info("Cross-Encoder 재순위 완료: %d개 후보 → %d개 선택", len(texts), len(selected))
            return selected
        except Exception as e:
            logger.warning("Cross-Encoder 재순위 실패 (폴백): %s", e)
            return texts[:top_k]


def _rrf_merge(
    vec_results: list[dict],
    bm25_results: list[tuple[str, float]],
    k: int = 60,
    top_n: int = 20,
) -> list[str]:
    scores: dict[str, float] = {}
    for rank, r in enumerate(vec_results):
        t = r["text"]
        scores[t] = scores.get(t, 0.0) + 1.0 / (k + rank + 1)
    for rank, (t, _) in enumerate(bm25_results):
        scores[t] = scores.get(t, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=lambda t: scores[t], reverse=True)[:top_n]


def _select_diverse_chunks(chunks: list[dict], top_k: int, diversity_window: int | None = None) -> list[dict]:
    window_size = diversity_window or top_k
    diversity_pool = chunks[:window_size]
    selected: list[dict] = []
    deferred: list[dict] = []
    seen_sources: set[str] = set()
    seen_texts: set[str] = set()

    for chunk in diversity_pool:
        text = chunk.get("text", "")
        if text in seen_texts:
            continue
        seen_texts.add(text)

        source = chunk.get("source_path", "")
        if source and source not in seen_sources and len(selected) < top_k:
            selected.append(chunk)
            seen_sources.add(source)
        else:
            deferred.append(chunk)

    for chunk in deferred + chunks[window_size:]:
        if len(selected) >= top_k:
            break
        text = chunk.get("text", "")
        if text in seen_texts:
            continue
        seen_texts.add(text)
        selected.append(chunk)

    return selected[:top_k]


class RAGEngine:
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_engine: EmbeddingEngine,
        llm: OllamaLLM,
        top_k: int = 5,
        max_context_chars: int = 8000,
        reranker_model: str | None = DEFAULT_RERANKER_MODEL,
    ):
        if top_k <= 0:
            raise ValueError(f"top_k는 양수여야 합니다: {top_k}")
        if max_context_chars <= 0:
            raise ValueError(f"max_context_chars는 양수여야 합니다: {max_context_chars}")
        self._store = vector_store
        self._embedder = embedding_engine
        self._llm = llm
        self._top_k = top_k
        self._max_context_chars = max_context_chars
        self._reranker = _CrossEncoderReranker(reranker_model) if reranker_model else None
        logger.info(
            "RAGEngine 초기화: top_k=%d, model=%s, max_context_chars=%d, reranker=%s",
            top_k, llm.model, max_context_chars,
            reranker_model or "None"
        )

    @property
    def llm(self) -> OllamaLLM:
        return self._llm

    @llm.setter
    def llm(self, llm: OllamaLLM) -> None:
        logger.info("RAGEngine LLM 변경: %s → %s", self._llm.model, llm.model)
        self._llm = llm

    def query(
        self,
        question: str,
        doc_type: str | None = None,
        *,
        answer_mode: str = "standard",
        trace_route: str = "rag.query",
        trace_metadata: dict | None = None,
        trace_enabled: bool = True,
    ) -> dict:
        if not question.strip():
            raise ValueError("question이 비어 있습니다")
        if answer_mode not in ANSWER_MODE_PROMPTS:
            raise ValueError(f"지원하지 않는 answer_mode입니다: {answer_mode}")

        logger.info("RAG 쿼리: %s (doc_type=%s, answer_mode=%s)", question, doc_type, answer_mode)

        should_trace = trace_enabled and is_trace_enabled()
        trace_id = new_trace_id() if should_trace else None
        trace_metadata = dict(trace_metadata or {})
        trace_metadata.setdefault("answer_mode", answer_mode)
        total_start = time.perf_counter()
        timings_ms: dict[str, float] = {}

        try:
            retrieval_start = time.perf_counter()
            final_chunks = self.retrieve(question, doc_type=doc_type, timings_ms=timings_ms)
            timings_ms["retrieval_total"] = _elapsed_ms(retrieval_start)

            if not final_chunks:
                logger.warning("최종 청크 없음")
                answer = NO_RESULTS_ANSWER
                timings_ms["total"] = _elapsed_ms(total_start)
                if should_trace:
                    trace_event(
                        route=trace_route,
                        trace_id=trace_id,
                        question=question,
                        doc_type=doc_type,
                        model=self._llm.model,
                        top_k=self._top_k,
                        retrieved_sources=[],
                        latency_ms=timings_ms,
                        answer_length=len(answer),
                        metadata=trace_metadata,
                    )
                return {"answer": answer, "sources": [], "query": question}

            # max_context_chars 제한으로 LLM 컨텍스트 창 초과 방지
            context_parts = []
            total_chars = 0
            for i, r in enumerate(final_chunks, 1):
                source = r.get("source_path", "출처 미상")
                part = f"[{i}] 출처: {source}\n{r['text']}"
                if total_chars + len(part) > self._max_context_chars:
                    logger.warning("컨텍스트 길이 제한 초과 — %d개 중 %d개 청크만 사용", len(final_chunks), i - 1)
                    break
                context_parts.append(part)
                total_chars += len(part)
            if not context_parts:
                r0 = final_chunks[0]
                context_parts.append(f"[1] 출처: {r0.get('source_path', '출처 미상')}\n{r0['text'][:self._max_context_chars]}")

            context = "\n\n".join(context_parts)
            prompt_template = ANSWER_MODE_PROMPTS[answer_mode]
            prompt = prompt_template.format(context=context, question=question)
            llm_start = time.perf_counter()
            answer = self._llm.predict(prompt)
            timings_ms["llm"] = _elapsed_ms(llm_start)
            logger.info("RAG 쿼리 완료: 소스 %d개, 답변 길이 %d", len(final_chunks), len(answer))

            sources = [
                {
                    "source_path": r.get("source_path", ""),
                    "text": r["text"],
                    "distance": r.get("distance", 0.0),
                }
                for r in final_chunks
            ]

            timings_ms["total"] = _elapsed_ms(total_start)
            if should_trace:
                trace_event(
                    route=trace_route,
                    trace_id=trace_id,
                    question=question,
                    doc_type=doc_type,
                    model=self._llm.model,
                    top_k=self._top_k,
                    retrieved_sources=sources,
                    latency_ms=timings_ms,
                    answer_length=len(answer),
                    metadata=trace_metadata,
                )

            return {"answer": answer, "sources": sources, "query": question}
        except Exception as e:
            if should_trace:
                timings_ms["total"] = _elapsed_ms(total_start)
                trace_event(
                    route=trace_route,
                    trace_id=trace_id,
                    question=question,
                    doc_type=doc_type,
                    model=self._llm.model,
                    top_k=self._top_k,
                    latency_ms=timings_ms,
                    error_type=type(e).__name__,
                    metadata=trace_metadata,
                )
            raise

    def retrieve(
        self,
        question: str,
        doc_type: str | None = None,
        *,
        timings_ms: dict[str, float] | None = None,
    ) -> list[dict]:
        if not question.strip():
            raise ValueError("question이 비어 있습니다")

        where = _doc_type_where(doc_type)
        embed_start = time.perf_counter()
        query_embedding = self._embedder.embed_query(question)
        if timings_ms is not None:
            timings_ms["embedding"] = _elapsed_ms(embed_start)
        vector_start = time.perf_counter()
        vec_results = self._store.similarity_search(query_embedding, k=self._top_k * 3, where=where)
        if timings_ms is not None:
            timings_ms["vector_search"] = _elapsed_ms(vector_start)

        if not vec_results:
            logger.warning("검색 결과 없음 — 컬렉션이 비어 있습니다")
            return []

        try:
            bm25_start = time.perf_counter()
            bm25_results = _bm25_cache.search(self._store, question, n=self._top_k * 3, where=where)
            if timings_ms is not None:
                timings_ms["bm25_search"] = _elapsed_ms(bm25_start)
        except Exception as e:
            logger.warning("BM25 검색 예외 (폴백): %s", e)
            bm25_results = []

        if bm25_results:
            merged_texts = _rrf_merge(vec_results, bm25_results, top_n=self._top_k * 4)
            if self._reranker:
                rerank_start = time.perf_counter()
                merged_texts = self._reranker.rerank(question, merged_texts, len(merged_texts))
                if timings_ms is not None:
                    timings_ms["rerank"] = _elapsed_ms(rerank_start)
            vec_dict = {r["text"]: r for r in vec_results}
            ranked_chunks: list[dict] = []
            for text in merged_texts:
                if text in vec_dict:
                    ranked_chunks.append(vec_dict[text])
                else:
                    doc = _bm25_cache.get_doc(text)
                    if doc:
                        ranked_chunks.append(doc)
            final_chunks = _select_diverse_chunks(
                ranked_chunks,
                self._top_k,
                diversity_window=self._top_k * 2 + 2,
            )
        else:
            final_chunks = _select_diverse_chunks(vec_results, self._top_k)

        return final_chunks
