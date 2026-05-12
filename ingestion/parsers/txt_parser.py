from pathlib import Path
from .base_parser import BaseParser, ParsedDocument


class TxtParser(BaseParser):
    @property
    def supported_extensions(self) -> list[str]:
        return [".txt"]

    def parse(self, file_path: Path) -> ParsedDocument:
        file_path = Path(file_path)
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        return ParsedDocument(
            content=text,
            source_path=str(file_path.resolve()),
            metadata={"parser": "TxtParser", "filename": file_path.name},
        )
