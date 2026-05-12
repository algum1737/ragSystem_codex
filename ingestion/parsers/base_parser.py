from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ParsedDocument:
    content: str
    source_path: str
    metadata: dict


class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> ParsedDocument:
        ...

    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        ...

    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.supported_extensions
