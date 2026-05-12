#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path

from ingestion.pipeline import IngestionPipeline


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ragSystem 문서 인제스천 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", help="인제스천할 파일 또는 디렉토리 경로")
    parser.add_argument("--db-path", default="./chroma_db", help="Chroma DB 저장 경로 (기본: ./chroma_db)")
    parser.add_argument("--collection", default="ragSystem", help="Chroma 컬렉션 이름 (기본: ragSystem)")
    parser.add_argument("--chunk-size", type=int, default=500, help="청크 크기 (기본: 500)")
    parser.add_argument("--chunk-overlap", type=int, default=50, help="청크 오버랩 (기본: 50)")
    parser.add_argument("--verbose", action="store_true", help="상세 로그 출력")
    args = parser.parse_args()

    _setup_logging(args.verbose)

    target = Path(args.path)
    if not target.exists():
        print(f"오류: 경로를 찾을 수 없습니다: {target}", file=sys.stderr)
        return 1

    pipeline = IngestionPipeline(
        db_path=args.db_path,
        collection_name=args.collection,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )

    if target.is_file():
        try:
            stats = pipeline.ingest(target)
            print(f"완료: {stats['chunks_added']}개 청크 저장 — {target.name} (파서: {stats['parser']})")
            return 0
        except (ValueError, RuntimeError) as e:
            print(f"오류: {e}", file=sys.stderr)
            return 1

    if target.is_dir():
        stats = pipeline.ingest_directory(target)
        print(
            f"완료: {stats['files_processed']}개 파일, {stats['chunks_added']}개 청크 저장"
            + (f" | 실패: {stats['files_failed']}개" if stats["files_failed"] else "")
        )
        for err in stats["errors"]:
            print(f"  실패: {err['file']} — {err['error']}", file=sys.stderr)
        return 0 if not stats["errors"] else 1

    print(f"오류: 파일 또는 디렉토리가 아닙니다: {target}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
