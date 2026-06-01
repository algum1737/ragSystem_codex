import json
import logging
import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

# 프로젝트 루트(eval/../)를 sys.path에 추가 — 서브디렉토리 실행 시 ingestion/retriever 임포트 가능
sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)

_DB_PATH = "./chroma_db"
_COLLECTION = "ragSystem"
_DOC_TYPE_ALIASES = {
    "일반": ["일반", "일반약관"],
    "위치기반서비스": ["위치기반서비스", "위치기반약관"],
}


def _tokenize_for_overlap(text: str) -> set[str]:
    tokens = re.findall(r"[가-힣]+|[a-zA-Z0-9]+", text.lower())
    return {t for t in tokens if len(t) > 1}


def _strip_citation_markers(text: str) -> str:
    cleaned = re.sub(r"\s*\[[0-9,\s]+\]", "", text)
    cleaned = re.sub(r"(,\s*){2,}", ", ", cleaned)
    cleaned = re.sub(r"\s+,", ",", cleaned)
    return cleaned.strip()


def _doc_type_where(doc_type: str | None) -> dict | None:
    if not doc_type:
        return None
    values = _DOC_TYPE_ALIASES.get(doc_type, [doc_type])
    return {"doc_type": values[0]} if len(values) == 1 else {"doc_type": {"$in": values}}


class RAGEvaluator:
    def __init__(self, top_k: int = 5, llm_model: str = "gemma3:12b"):
        from ingestion.vector_store import VectorStore
        from ingestion.embedder import EmbeddingEngine

        self._top_k = top_k
        self._llm_model = llm_model
        self._store = VectorStore(db_path=_DB_PATH, collection_name=_COLLECTION)
        self._embedder = EmbeddingEngine()
        # OllamaLLM/RAGEngine lazy — only initialized when accuracy/faithfulness is needed
        self._llm = None
        self._engine = None
        logger.info("RAGEvaluator 초기화: top_k=%d, model=%s", top_k, llm_model)

    def _get_engine(self):
        if self._engine is None:
            from retriever.llm import OllamaLLM
            from retriever.engine import RAGEngine

            self._llm = OllamaLLM(model=self._llm_model)
            self._engine = RAGEngine(
                vector_store=self._store,
                embedding_engine=self._embedder,
                llm=self._llm,
                top_k=self._top_k,
            )
        return self._engine

    def _retrieval_query(self, question: str, doc_type: str | None = None) -> list[str]:
        """Vector-only retrieval path — Ollama 불필요."""
        embedding = self._embedder.embed_query(question)
        where = _doc_type_where(doc_type)
        results = self._store.similarity_search(embedding, k=self._top_k, where=where)
        return [r.get("source_path", "") for r in results]

    def _rag_retrieval_query(self, question: str, doc_type: str | None = None) -> tuple[list[str], list[str]]:
        """RAG retrieval path without LLM generation."""
        chunks = self._get_engine().retrieve(question, doc_type=doc_type)
        sources = [c.get("source_path", "") for c in chunks]
        texts = [c.get("text", "") for c in chunks]
        return sources, texts

    def _load_cases(self) -> list[dict]:
        cases_path = Path(__file__).parent / "test_cases.json"
        with open(cases_path, encoding="utf-8") as f:
            data = json.load(f)
        return data["cases"]

    def precision_at_k(
        self,
        retrieved_sources: list[str],
        relevant_sources: list[str],
        k: int,
    ) -> float | None:
        if not relevant_sources:
            return None
        retrieved_basenames = {unicodedata.normalize("NFC", os.path.basename(s)) for s in retrieved_sources[:k]}
        relevant_basenames = {unicodedata.normalize("NFC", os.path.basename(s)) for s in relevant_sources}
        intersection = retrieved_basenames & relevant_basenames
        return len(intersection) / k

    def normalized_source_precision_at_k(
        self,
        retrieved_sources: list[str],
        relevant_sources: list[str],
        k: int,
    ) -> float | None:
        if not relevant_sources:
            return None
        retrieved_basenames = {unicodedata.normalize("NFC", os.path.basename(s)) for s in retrieved_sources[:k]}
        relevant_basenames = {unicodedata.normalize("NFC", os.path.basename(s)) for s in relevant_sources}
        denominator = min(k, len(relevant_basenames))
        if denominator <= 0:
            return None
        intersection = retrieved_basenames & relevant_basenames
        return len(intersection) / denominator

    def chunk_precision_at_k(
        self,
        retrieved_sources: list[str],
        relevant_sources: list[str],
        k: int,
    ) -> float | None:
        if not relevant_sources:
            return None
        relevant_basenames = {unicodedata.normalize("NFC", os.path.basename(s)) for s in relevant_sources}
        retrieved_basenames = [
            unicodedata.normalize("NFC", os.path.basename(s))
            for s in retrieved_sources[:k]
        ]
        if not retrieved_basenames:
            return 0.0
        matched = sum(1 for source in retrieved_basenames if source in relevant_basenames)
        return matched / k

    def source_coverage_at_k(
        self,
        retrieved_sources: list[str],
        relevant_sources: list[str],
        k: int,
    ) -> float | None:
        if not relevant_sources:
            return None
        retrieved_basenames = {unicodedata.normalize("NFC", os.path.basename(s)) for s in retrieved_sources[:k]}
        relevant_basenames = {unicodedata.normalize("NFC", os.path.basename(s)) for s in relevant_sources}
        if not relevant_basenames:
            return None
        return len(retrieved_basenames & relevant_basenames) / len(relevant_basenames)

    def _is_not_found_answer(self, answer: str | None) -> bool:
        if not answer:
            return False
        normalized = answer.strip()
        if "찾을 수 없습니다" in normalized:
            return True
        # Partial answers may contain a separate "not confirmed" section.
        # Treat it as no-answer only when the whole response starts that way.
        no_answer_prefixes = (
            "문서에서 확인되지 않는 내용입니다",
            "제공된 문서에는",
            "제공된 문서에서 확인되지 않습니다",
        )
        return normalized.startswith(no_answer_prefixes)

    def expected_not_found_accuracy(self, answer: str | None, expected_not_found: bool) -> float | None:
        if not expected_not_found:
            return None
        return 1.0 if self._is_not_found_answer(answer) else 0.0

    def answer_accuracy(self, answer: str, expected_keywords: list[str | list[str]]) -> float | None:
        if not expected_keywords:
            return None
        answer_lower = answer.lower().strip()
        matched = 0
        for keyword in expected_keywords:
            if isinstance(keyword, list):
                if any(str(kw).lower().strip() in answer_lower for kw in keyword):
                    matched += 1
            elif str(keyword).lower().strip() in answer_lower:
                matched += 1
        return matched / len(expected_keywords)

    def _select_faithfulness_contexts(
        self,
        question: str,
        answer: str,
        context_texts: list[str],
        context_sources: list[str] | None = None,
        max_contexts: int = 5,
    ) -> list[str]:
        if len(context_texts) <= max_contexts:
            return context_texts

        query_tokens = _tokenize_for_overlap(f"{question}\n{answer}")
        if not query_tokens:
            return context_texts[:max_contexts]

        scored: list[tuple[int, int, str, str]] = []
        for index, text in enumerate(context_texts):
            text_tokens = _tokenize_for_overlap(text)
            overlap = len(query_tokens & text_tokens)
            source = context_sources[index] if context_sources and index < len(context_sources) else ""
            source = unicodedata.normalize("NFC", os.path.basename(source))
            scored.append((overlap, -index, source, text))

        selected: list[tuple[int, int, str, str]] = []
        seen_sources: set[str] = set()
        for item in sorted(scored, reverse=True):
            source = item[2]
            if source and source in seen_sources:
                continue
            selected.append(item)
            if source:
                seen_sources.add(source)
            if len(selected) >= max_contexts:
                break

        if len(selected) < max_contexts:
            selected_texts = {item[3] for item in selected}
            for item in sorted(scored, reverse=True):
                if item[3] in selected_texts:
                    continue
                selected.append(item)
                selected_texts.add(item[3])
                if len(selected) >= max_contexts:
                    break

        # Keep retrieval order inside the final prompt after relevance and source filtering.
        selected_texts = [text for _, _, _, text in sorted(selected, key=lambda item: -item[1])]
        return selected_texts

    def faithfulness(
        self,
        question: str,
        answer: str,
        context_texts: list[str],
        context_sources: list[str] | None = None,
    ) -> float | None:
        if not context_texts:
            return None
        selected_contexts = self._select_faithfulness_contexts(
            question,
            answer,
            context_texts,
            context_sources=context_sources,
        )
        context = "\n\n".join(selected_contexts)
        prompt = (
            "다음 답변이 참고 문서에만 근거하는지 판단하세요.\n\n"
            f"[참고 문서]\n{context}\n\n"
            f"[답변]\n{_strip_citation_markers(answer)}\n\n"
            '"YES" 또는 "NO"로만 답하세요.'
        )
        try:
            self._get_engine()
            result = self._llm.predict(prompt)
            result_upper = result.strip().upper()
            if "YES" in result_upper:
                return 1.0
            elif "NO" in result_upper:
                return 0.0
            logger.warning("Faithfulness 판정 파싱 실패: %r", result)
            return None
        except Exception as e:
            logger.warning("Faithfulness LLM 호출 실패: %s", e)
            return None

    def run(self, metrics: list[str] | None = None) -> dict:
        if metrics is None:
            metrics = ["retrieval", "accuracy", "faithfulness"]

        stats = self._store.get_stats()
        if stats.get("count", 0) == 0:
            print("⚠️  Chroma DB가 비어 있습니다. 먼저 문서를 인제스천하세요.")
            sys.exit(1)

        cases = self._load_cases()
        need_llm = any(m in metrics for m in ["accuracy", "faithfulness"])

        print(f"평가 시작: {len(cases)}개 케이스, 지표: {metrics}")

        results = []
        for i, case in enumerate(cases, 1):
            print(f"  케이스 {i}/{len(cases)}: {case['question'][:40]}...")
            case_result: dict = {
                "id": case["id"],
                "question": case["question"],
                "precision_at_k": None,
                "vector_precision_at_k": None,
                "rag_precision_at_k": None,
                "normalized_source_precision_at_k": None,
                "vector_normalized_source_precision_at_k": None,
                "rag_normalized_source_precision_at_k": None,
                "vector_chunk_precision_at_k": None,
                "rag_chunk_precision_at_k": None,
                "source_recall_at_k": None,
                "source_coverage_at_k": None,
                "answer_accuracy": None,
                "faithfulness": None,
                "not_found": None,
                "expected_not_found": case.get("expected_not_found", False),
                "not_found_success": None,
            }

            if "retrieval" in metrics:
                retrieved = self._retrieval_query(case["question"], doc_type=case.get("doc_type"))
                case_result["vector_retrieved_sources"] = retrieved
                # Backward-compatible alias for older report consumers.
                case_result["retrieved_sources"] = retrieved
                vector_precision = self.precision_at_k(
                    retrieved, case.get("relevant_sources", []), self._top_k
                )
                case_result["vector_precision_at_k"] = vector_precision
                # Backward-compatible metric alias for older reports.
                case_result["precision_at_k"] = vector_precision
                vector_normalized_precision = self.normalized_source_precision_at_k(
                    retrieved, case.get("relevant_sources", []), self._top_k
                )
                case_result["vector_normalized_source_precision_at_k"] = vector_normalized_precision
                # Backward-compatible path alias follows the vector-only default precision path.
                case_result["normalized_source_precision_at_k"] = vector_normalized_precision
                case_result["vector_chunk_precision_at_k"] = self.chunk_precision_at_k(
                    retrieved, case.get("relevant_sources", []), self._top_k
                )
                try:
                    rag_sources, rag_context_texts = self._rag_retrieval_query(
                        case["question"], doc_type=case.get("doc_type")
                    )
                    case_result["rag_retrieved_sources"] = rag_sources
                    case_result["rag_precision_at_k"] = self.precision_at_k(
                        rag_sources, case.get("relevant_sources", []), self._top_k
                    )
                    case_result["rag_normalized_source_precision_at_k"] = self.normalized_source_precision_at_k(
                        rag_sources, case.get("relevant_sources", []), self._top_k
                    )
                    case_result["rag_chunk_precision_at_k"] = self.chunk_precision_at_k(
                        rag_sources, case.get("relevant_sources", []), self._top_k
                    )
                    case_result["source_coverage_at_k"] = self.source_coverage_at_k(
                        rag_sources, case.get("relevant_sources", []), self._top_k
                    )
                    # Clearer alias for report consumers: this is source-level recall, not precision.
                    case_result["source_recall_at_k"] = case_result["source_coverage_at_k"]
                except Exception as e:
                    logger.warning("RAG retrieval 실패 (케이스 %s): %s", case["id"], e)
                    rag_sources = []
                    rag_context_texts = []
            else:
                rag_sources = []
                rag_context_texts = []

            if need_llm:
                try:
                    rag_result = self._get_engine().query(case["question"], doc_type=case.get("doc_type"))
                    answer = rag_result.get("answer", "")
                    context_texts = [s["text"] for s in rag_result.get("sources", [])]
                    query_sources = [s.get("source_path", "") for s in rag_result.get("sources", [])]
                    if not rag_sources:
                        rag_sources = query_sources
                    case_result["answer"] = answer
                    case_result["rag_retrieved_sources"] = rag_sources
                    case_result["not_found"] = self._is_not_found_answer(answer)
                    if case_result["expected_not_found"]:
                        case_result["not_found_success"] = case_result["not_found"] is True
                except Exception as e:
                    logger.warning("RAG query 실패 (케이스 %s): %s", case["id"], e)
                    answer = None
                    context_texts = rag_context_texts
            else:
                answer = None
                context_texts = rag_context_texts

            if "accuracy" in metrics and answer is not None:
                expected_not_found_accuracy = self.expected_not_found_accuracy(
                    answer,
                    case_result["expected_not_found"],
                )
                case_result["answer_accuracy"] = (
                    expected_not_found_accuracy
                    if expected_not_found_accuracy is not None
                    else self.answer_accuracy(answer, case.get("expected_keywords", []))
                )

            if "faithfulness" in metrics and answer is not None:
                if case_result["expected_not_found"] and case_result["not_found"] is True:
                    case_result["faithfulness"] = 1.0
                else:
                    case_result["faithfulness"] = self.faithfulness(
                        case["question"],
                        answer,
                        context_texts,
                        context_sources=query_sources if need_llm else rag_sources,
                    )

            results.append(case_result)

        def _mean(key: str) -> float | None:
            vals = [r[key] for r in results if r.get(key) is not None]
            return round(sum(vals) / len(vals), 4) if vals else None

        summary = {
            "total_cases": len(cases),
            "metrics_evaluated": metrics,
            "llm_model": self._llm_model,
            "top_k": self._top_k,
            "precision@k_mean": _mean("precision_at_k"),
            "vector_precision@k_mean": _mean("vector_precision_at_k"),
            "rag_precision@k_mean": _mean("rag_precision_at_k"),
            "normalized_source_precision@k_mean": _mean("normalized_source_precision_at_k"),
            "vector_normalized_source_precision@k_mean": _mean("vector_normalized_source_precision_at_k"),
            "rag_normalized_source_precision@k_mean": _mean("rag_normalized_source_precision_at_k"),
            "vector_chunk_precision@k_mean": _mean("vector_chunk_precision_at_k"),
            "rag_chunk_precision@k_mean": _mean("rag_chunk_precision_at_k"),
            "source_recall@k_mean": _mean("source_recall_at_k"),
            "source_coverage@k_mean": _mean("source_coverage_at_k"),
            "accuracy_mean": _mean("answer_accuracy"),
            "faithfulness_mean": _mean("faithfulness"),
            "not_found_rate": _mean("not_found"),
            "not_found_success_rate": _mean("not_found_success"),
        }

        print("\n=== 평가 요약 ===")
        for k, v in summary.items():
            print(f"  {k}: {v}")

        return {"cases": results, "summary": summary}

    def save_report(self, results: dict, out_dir: str = "eval/results") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"eval_{timestamp}.json"

        try:
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, filename)
        except PermissionError as e:
            logger.warning("eval/results/ 생성 실패: %s — 현재 디렉토리에 저장 시도", e)
            out_path = f"eval_fallback_{timestamp}.json"

        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"리포트 저장 완료: {out_path}")
            return out_path
        except PermissionError as e:
            logger.error("리포트 저장 실패: %s", e)
            print(f"❌ 리포트 저장 실패: {e}")
            return ""


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s:%(name)s:%(message)s")

    parser = argparse.ArgumentParser(description="RAG 평가 파이프라인")
    parser.add_argument(
        "--metric",
        choices=["retrieval", "accuracy", "faithfulness"],
        help="단일 지표 측정 (리포트 저장 없음)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="전체 지표 측정 + eval/results/에 리포트 저장",
    )
    parser.add_argument("--top-k", type=int, default=5, dest="top_k")
    parser.add_argument("--model", default="gemma3:12b")
    args = parser.parse_args()

    evaluator = RAGEvaluator(top_k=args.top_k, llm_model=args.model)

    if args.all:
        result = evaluator.run()
        evaluator.save_report(result)
    elif args.metric:
        evaluator.run(metrics=[args.metric])
    else:
        parser.print_help()
