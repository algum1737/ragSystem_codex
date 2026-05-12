import logging
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .base_parser import BaseParser, ParsedDocument

logger = logging.getLogger(__name__)


class HwpParser(BaseParser):
    supported_extensions = [".hwp"]

    def parse(self, file_path: Path) -> ParsedDocument:
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        try:
            return self._parse_with_pyhwp(file_path)
        except (FileNotFoundError, PermissionError):
            raise  # 파일시스템 에러는 fallback 금지
        except Exception as pyhwp_err:
            logger.warning("pyhwp 실패, LibreOffice fallback 시도: %s — %s", file_path, pyhwp_err)
            return self._parse_with_libreoffice(file_path, pyhwp_err)

    def _parse_with_pyhwp(self, file_path: Path) -> ParsedDocument:
        from hwp5.hwp5txt import Hwp5File
        hwpfile = Hwp5File(str(file_path))
        raw = hwpfile.preview_text.text
        content = re.sub(r'\s+', ' ', raw).strip()
        if not content:
            logger.warning("빈 콘텐츠 추출됨 (pyhwp): %s", file_path)
        return ParsedDocument(
            content=content,
            source_path=str(file_path.resolve()),
            metadata={
                "file_name": file_path.name,
                "file_size_bytes": file_path.stat().st_size,
                "parser": "pyhwp",
            },
        )

    def _parse_with_libreoffice(self, file_path: Path, original_err: Exception) -> ParsedDocument:
        soffice = shutil.which("soffice")
        if not soffice:
            raise RuntimeError(
                f"HWP 파싱 실패: pyhwp와 LibreOffice 모두 사용 불가 — {file_path}"
            ) from original_err

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                result = subprocess.run(
                    [soffice, "--headless", "--convert-to", "docx",
                     "--outdir", tmpdir, str(file_path.resolve())],
                    capture_output=True, text=True, timeout=60,
                )
            except subprocess.TimeoutExpired as e:
                raise RuntimeError(
                    f"LibreOffice 변환 타임아웃 (60초 초과): {file_path}"
                ) from e

            if result.returncode != 0:
                raise RuntimeError(
                    f"LibreOffice 변환 실패: {file_path} — {result.stderr[:500]}"
                ) from original_err

            converted = next(Path(tmpdir).glob("*.docx"), None)
            if not converted:
                raise RuntimeError(
                    f"LibreOffice 변환 후 docx 파일 없음: {file_path}"
                ) from original_err

            from .docx_parser import DocxParser
            doc_result = DocxParser().parse(converted)
            return ParsedDocument(
                content=doc_result.content,
                source_path=str(file_path.resolve()),
                metadata={
                    "file_name": file_path.name,
                    "file_size_bytes": file_path.stat().st_size,
                    "parser": "libreoffice",
                },
            )
