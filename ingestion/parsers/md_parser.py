import re
from pathlib import Path
from .base_parser import BaseParser, ParsedDocument


def _strip_markdown(text: str) -> str:
    text = re.sub(r"```[^\n]*\n(.*?)```", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}([^_]+)_{1,3}", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^\)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^[-*=]{3,}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*[-+*]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class MdParser(BaseParser):
    @property
    def supported_extensions(self) -> list[str]:
        return [".md", ".markdown"]

    def parse(self, file_path: Path) -> ParsedDocument:
        file_path = Path(file_path)
        try:
            raw = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw = file_path.read_text(encoding="utf-8", errors="replace")
        text = _strip_markdown(raw)
        return ParsedDocument(
            content=text,
            source_path=str(file_path.resolve()),
            metadata={"parser": "MdParser", "filename": file_path.name},
        )
