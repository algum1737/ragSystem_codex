import logging
import re
from pathlib import Path

import pymupdf

from .base_parser import BaseParser, ParsedDocument

logger = logging.getLogger(__name__)


class PdfParser(BaseParser):
    @property
    def supported_extensions(self) -> list[str]:
        return [".pdf"]

    def parse(self, file_path: Path) -> ParsedDocument:
        try:
            doc = pymupdf.open(file_path)
        except Exception as e:
            raise RuntimeError(f"PDF 파일 열기 실패: {file_path}") from e

        if doc.needs_pass:
            raise ValueError(f"암호화된 PDF는 지원하지 않습니다: {file_path}")

        pages = [page.get_text() for page in doc]
        raw_content = " ".join(pages)
        content = re.sub(r'\s+', ' ', raw_content).strip()

        if not content:
            logger.warning("빈 콘텐츠 추출됨 (이미지 전용 PDF일 수 있음): %s", file_path)

        metadata = {
            "page_count": len(doc),
            "file_name": file_path.name,
            "file_size_bytes": file_path.stat().st_size,
            "parser": "pymupdf",
        }
        doc.close()

        source_path = str(file_path.resolve())
        return ParsedDocument(content=content, source_path=source_path, metadata=metadata)
