#!/usr/bin/env python3
import argparse
import logging
import sys

from ingestion.embedder import EmbeddingEngine
from ingestion.vector_store import VectorStore
from retriever.engine import RAGEngine
from retriever.llm import OllamaLLM


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ragSystem 자연어 질의 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("question", help="자연어 질문")
    parser.add_argument("--model", default="gemma3:12b", help="Ollama 모델명 (기본: gemma3:12b)")
    parser.add_argument("--ollama-url", default="http://localhost:11434", help="Ollama 서버 URL")
    parser.add_argument("--db-path", default="./chroma_db", help="Chroma DB 경로 (기본: ./chroma_db)")
    parser.add_argument("--collection", default="ragSystem", help="Chroma 컬렉션 이름")
    parser.add_argument("--top-k", type=int, default=5, help="검색할 청크 수 (기본: 5)")
    parser.add_argument("--verbose", action="store_true", help="상세 로그 출력")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="파이프라인 초기화만 확인 (LLM 호출 없음)",
    )
    args = parser.parse_args()

    _setup_logging(args.verbose)

    try:
        store = VectorStore(db_path=args.db_path, collection_name=args.collection)

        # dry-run 시 EmbeddingEngine 로딩(~30초) 불필요 — VectorStore 확인만으로 충분
        if args.dry_run:
            stats = store.get_stats()
            print(f"파이프라인 초기화 OK — 컬렉션: {stats['collection_name']}, 청크 수: {stats['count']}")
            return 0

        embedder = EmbeddingEngine()
        llm = OllamaLLM(model=args.model, base_url=args.ollama_url)
        engine = RAGEngine(
            vector_store=store,
            embedding_engine=embedder,
            llm=llm,
            top_k=args.top_k,
        )

        result = engine.query(args.question, trace_route="cli.query")

        print(f"\n답변:\n{result['answer']}\n")
        if result["sources"]:
            print("출처:")
            for i, src in enumerate(result["sources"], 1):
                print(f"  [{i}] {src['source_path']} (거리: {src['distance']:.4f})")
        else:
            print("(검색된 문서 없음)")

        return 0

    except (ValueError, RuntimeError) as e:
        print(f"오류: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
