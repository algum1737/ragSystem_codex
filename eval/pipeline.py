import json
import logging
import os
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
        return "찾을 수 없습니다" in answer

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

    def faithfulness(self, answer: str, context_texts: list[str]) -> float | None:
        if not context_texts:
            return None
        context = "\n\n".join(context_texts[:3])
        prompt = (
            "다음 답변이 참고 문서에만 근거하는지 판단하세요.\n\n"
            f"[참고 문서]\n{context}\n\n"
            f"[답변]\n{answer}\n\n"
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
                "source_coverage_at_k": None,
                "answer_accuracy": None,
                "faithfulness": None,
                "not_found": None,
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
                try:
                    rag_sources, rag_context_texts = self._rag_retrieval_query(
                        case["question"], doc_type=case.get("doc_type")
                    )
                    case_result["rag_retrieved_sources"] = rag_sources
                    case_result["rag_precision_at_k"] = self.precision_at_k(
                        rag_sources, case.get("relevant_sources", []), self._top_k
                    )
                    case_result["source_coverage_at_k"] = self.source_coverage_at_k(
                        rag_sources, case.get("relevant_sources", []), self._top_k
                    )
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
                except Exception as e:
                    logger.warning("RAG query 실패 (케이스 %s): %s", case["id"], e)
                    answer = None
                    context_texts = rag_context_texts
            else:
                answer = None
                context_texts = rag_context_texts

            if "accuracy" in metrics and answer is not None:
                case_result["answer_accuracy"] = self.answer_accuracy(
                    answer, case.get("expected_keywords", [])
                )

            if "faithfulness" in metrics and answer is not None:
                case_result["faithfulness"] = self.faithfulness(answer, context_texts)

            results.append(case_result)

        def _mean(key: str) -> float | None:
            vals = [r[key] for r in results if r.get(key) is not None]
            return round(sum(vals) / len(vals), 4) if vals else None

        summary = {
            "total_cases": len(cases),
            "metrics_evaluated": metrics,
            "precision@k_mean": _mean("precision_at_k"),
            "vector_precision@k_mean": _mean("vector_precision_at_k"),
            "rag_precision@k_mean": _mean("rag_precision_at_k"),
            "source_coverage@k_mean": _mean("source_coverage_at_k"),
            "accuracy_mean": _mean("answer_accuracy"),
            "faithfulness_mean": _mean("faithfulness"),
            "not_found_rate": _mean("not_found"),
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
