import logging
from pathlib import Path

from .chunker import TextChunker
from .embedder import EmbeddingEngine
from .vector_store import VectorStore
from .parsers import PdfParser, DocxParser, HwpParser, TxtParser, MdParser
from .parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)

DEFAULT_PARSERS: list[BaseParser] = [PdfParser(), DocxParser(), HwpParser(), TxtParser(), MdParser()]


class IngestionPipeline:
    def __init__(
        self,
        db_path: str = "./chroma_db",
        collection_name: str = "ragSystem",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self._parsers = list(DEFAULT_PARSERS)
        self._chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self._embedder = EmbeddingEngine()
        self._store = VectorStore(db_path=db_path, collection_name=collection_name)

    def _find_parser(self, file_path: Path) -> BaseParser | None:
        for parser in self._parsers:
            if parser.can_parse(file_path):
                return parser
        return None

    def ingest(self, file_path: Path, source_name: str | None = None, doc_type: str | None = None) -> dict:
        file_path = Path(file_path)
        parser = self._find_parser(file_path)
        if parser is None:
            raise ValueError(f"지원하지 않는 파일 형식: {file_path.suffix} ({file_path.name})")

        logger.info("인제스천 시작: %s", source_name or file_path.name)
        parsed = parser.parse(file_path)
        effective_source = source_name if source_name else parsed.source_path
        effective_metadata = {**parsed.metadata}
        if doc_type:
            effective_metadata["doc_type"] = doc_type
        chunks = self._chunker.split(parsed.content, effective_source, effective_metadata)

        if not chunks:
            logger.warning("청크 없음 (빈 문서일 수 있음): %s", source_name or file_path.name)
            return {"chunks_added": 0, "source_path": effective_source, "parser": effective_metadata.get("parser", "unknown")}

        embeddings = self._embedder.embed_chunks(chunks)
        added = self._store.add_chunks(chunks, embeddings)
        logger.info("인제스천 완료: %d개 청크 저장 — %s", added, source_name or file_path.name)
        return {
            "chunks_added": added,
            "source_path": effective_source,
            "parser": effective_metadata.get("parser", "unknown"),
        }

    def ingest_directory(self, dir_path: Path) -> dict:
        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            raise ValueError(f"디렉토리가 아닙니다: {dir_path}")

        supported_extensions = set()
        for parser in self._parsers:
            supported_extensions.update(parser.supported_extensions)

        entries = list(dir_path.iterdir())
        for entry in entries:
            if entry.is_dir():
                logger.warning("서브디렉토리 건너뜀 (재귀 미지원): %s", entry.name)
        files = [f for f in entries if f.is_file() and f.suffix.lower() in supported_extensions]
        total_chunks = 0
        errors = []

        for file_path in files:
            try:
                result = self.ingest(file_path)
                total_chunks += result["chunks_added"]
            except Exception as e:
                logger.error("인제스천 실패: %s — %s", file_path.name, e)
                errors.append({"file": str(file_path), "error": str(e)})

        return {
            "files_processed": len(files) - len(errors),
            "files_failed": len(errors),
            "chunks_added": total_chunks,
            "errors": errors,
        }
