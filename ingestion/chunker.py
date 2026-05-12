from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class Chunk:
    text: str
    source_path: str
    metadata: dict
    chunk_index: int


# 한국어 문장 종결 패턴을 앞에 배치해 자연어 경계 우선 분할
_KO_SEPARATORS = [
    "\n\n",   # 단락 경계 (최우선)
    "\n",     # 줄 바꿈
    "다. ",   # 한국어 평서문 종결
    "요. ",   # 한국어 경어 종결
    "다.\n",
    "요.\n",
    "다!",
    "요!",
    "다?",
    "요?",
    ". ",     # 영문 문장 종결
    " ",      # 단어 경계
    "",       # 문자 단위 (최후)
]


class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        if chunk_size <= 0:
            raise ValueError(f"chunk_size는 양수여야 합니다: {chunk_size}")
        if chunk_overlap >= chunk_size:
            raise ValueError(f"chunk_overlap({chunk_overlap})은 chunk_size({chunk_size})보다 작아야 합니다")
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=_KO_SEPARATORS,
            length_function=len,
            is_separator_regex=False,
        )

    def split(self, text: str, source_path: str, metadata: dict) -> list[Chunk]:
        if not text:
            return []
        raw_chunks = self._splitter.split_text(text)
        valid_chunks = [c for c in raw_chunks if c.strip()]
        total = len(valid_chunks)
        return [
            Chunk(
                text=chunk,
                source_path=source_path,
                metadata={**metadata, "chunk_index": i, "total_chunks": total},
                chunk_index=i,
            )
            for i, chunk in enumerate(valid_chunks)
        ]
