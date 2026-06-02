import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_TRACE_PATH = "./logs/rag_traces.jsonl"
TRUE_VALUES = {"1", "true", "yes", "on"}


def is_trace_enabled() -> bool:
    return os.getenv("RAG_TRACE_ENABLED", "").strip().lower() in TRUE_VALUES


def new_trace_id() -> str:
    return str(uuid.uuid4())


def _trace_path() -> Path:
    return Path(os.getenv("RAG_TRACE_PATH", DEFAULT_TRACE_PATH))


def _hash_text(text: str | None) -> str | None:
    if text is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _include_preview() -> bool:
    return os.getenv("RAG_TRACE_INCLUDE_PREVIEW", "").strip().lower() in TRUE_VALUES


def _preview(text: str | None, limit: int = 120) -> str | None:
    if text is None or not _include_preview():
        return None
    normalized = " ".join(text.split())
    return normalized[:limit]


def _source_path(item: Any) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return str(item.get("source_path", ""))
    return ""


def make_trace_event(
    *,
    route: str,
    trace_id: str | None = None,
    question: str | None = None,
    doc_type: str | None = None,
    model: str | None = None,
    top_k: int | None = None,
    retrieved_sources: list[Any] | None = None,
    latency_ms: dict[str, float] | None = None,
    answer: str | None = None,
    answer_length: int | None = None,
    error_type: str | None = None,
    eval_case_id: str | None = None,
    eval_scores: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event: dict[str, Any] = {
        "schema_version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trace_id": trace_id or new_trace_id(),
        "route": route,
    }
    if question is not None:
        event["question_hash"] = _hash_text(question)
        question_preview = _preview(question)
        if question_preview is not None:
            event["question_preview"] = question_preview
    if doc_type is not None:
        event["doc_type"] = doc_type
    if model is not None:
        event["model"] = model
    if top_k is not None:
        event["top_k"] = top_k
    if retrieved_sources is not None:
        event["retrieved_sources"] = [_source_path(s) for s in retrieved_sources]
    if latency_ms is not None:
        event["latency_ms"] = {k: round(float(v), 2) for k, v in latency_ms.items()}
    if answer_length is not None:
        event["answer_length"] = answer_length
    elif answer is not None:
        event["answer_length"] = len(answer)
    if error_type is not None:
        event["error_type"] = error_type
    if eval_case_id is not None:
        event["eval_case_id"] = eval_case_id
    if eval_scores is not None:
        event["eval_scores"] = eval_scores
    if metadata:
        event["metadata"] = metadata
    return event


def write_trace_event(event: dict[str, Any]) -> None:
    try:
        path = _trace_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False, sort_keys=True))
            f.write("\n")
    except Exception as e:
        logger.warning("trace event 기록 실패: %s", e)


def trace_event(**kwargs: Any) -> str | None:
    if not is_trace_enabled():
        return None
    event = make_trace_event(**kwargs)
    write_trace_event(event)
    return str(event["trace_id"])
