from pydantic import BaseModel, field_validator


class HealthResponse(BaseModel):
    status: str
    model: str


class StatsResponse(BaseModel):
    collection_name: str
    count: int


_VALID_DOC_TYPES = {None, "일반약관", "위치기반약관"}


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    doc_type: str | None = None

    @field_validator("question")
    @classmethod
    def question_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("question은 비어 있을 수 없습니다")
        return v

    @field_validator("top_k")
    @classmethod
    def top_k_range(cls, v: int) -> int:
        # audit-added: 상한 없으면 top_k=10000 시 Chroma 부하 + 거대 프롬프트 조립
        if v <= 0:
            raise ValueError("top_k는 양수여야 합니다")
        if v > 20:
            raise ValueError("top_k는 20 이하여야 합니다")
        return v

    @field_validator("doc_type")
    @classmethod
    def doc_type_valid(cls, v: str | None) -> str | None:
        if v not in _VALID_DOC_TYPES:
            raise ValueError(f"유효하지 않은 doc_type: {v!r}. 허용 값: 일반약관, 위치기반약관")
        return v


class SourceItem(BaseModel):
    source_path: str
    text: str
    distance: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    query: str


class IngestResponse(BaseModel):
    chunks_added: int
    source_path: str
    parser: str


class GenerateRequest(BaseModel):
    project_name: str
    sections: list[str] = []


class GenerateResponse(BaseModel):
    task_id: str
    status: str
    estimated_seconds: int


class StatusResponse(BaseModel):
    task_id: str
    status: str
    progress: int
    current_section: str = ""
    error: str = ""


class DownloadInfo(BaseModel):
    task_id: str
    output_path: str


class ModelChangeRequest(BaseModel):
    model: str

    @field_validator("model")
    @classmethod
    def model_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("model은 비어 있을 수 없습니다")
        return v


class ModelChangeResponse(BaseModel):
    model: str
    previous_model: str


class PullRequest(BaseModel):
    model: str

    @field_validator("model")
    @classmethod
    def model_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("model은 비어 있을 수 없습니다")
        return v


class PullResponse(BaseModel):
    pull_id: str
    model: str
    status: str


class PullStatusResponse(BaseModel):
    pull_id: str
    model: str
    status: str  # "pulling" | "completed" | "failed"
    progress: int
    current_status: str = ""
    error: str = ""


class ModelDeleteRequest(BaseModel):
    model: str

    @field_validator("model")
    @classmethod
    def model_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("model은 비어 있을 수 없습니다")
        return v


class ModelDeleteResponse(BaseModel):
    model: str
    deleted: bool


class ResetResponse(BaseModel):
    reset: bool
    collection_name: str
