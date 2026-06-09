#!/usr/bin/env python3
"""Compare concise RAG prompt candidates against the current prompt."""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import retriever.engine as engine_mod
from ingestion.embedder import EmbeddingEngine
from ingestion.vector_store import VectorStore
from retriever.engine import RAGEngine
from retriever.llm import OllamaLLM


CONCISE_BULLET_TEMPLATE = """당신은 주어진 참고 문서만 근거로 답변하는 한국어 지식 어시스턴트입니다.

답변 규칙:
1. 반드시 한국어로 답변하세요.
2. 참고 문서에 있는 내용만 사용하고 추측하지 마세요.
3. 질문에 직접 답하는 핵심만 3~5개 bullet로 작성하세요.
4. 각 bullet은 1문장으로 제한하세요.
5. 문서에서 확인되지 않는 내용은 별도 bullet로 "문서에서 확인되지 않습니다"라고 쓰세요.
6. 마지막 줄에 "근거: 문서명1, 문서명2" 형식으로 사용한 출처명을 짧게 적으세요.
7. 불필요한 배경 설명, 반복, 원문 긴 인용은 쓰지 마세요.

[참고 문서]
{context}

[질문]
{question}

[답변]"""


REFINED_CONCISE_BULLET_TEMPLATE = """당신은 주어진 참고 문서만 근거로 답변하는 한국어 지식 어시스턴트입니다.

답변 규칙:
1. 반드시 한국어로 답변하세요.
2. 참고 문서에 있는 내용만 사용하고 추측하지 마세요.
3. 첫 줄부터 질문에 직접 답하는 핵심만 3~4개 bullet로 작성하세요.
4. 각 bullet은 1문장으로 제한하세요.
5. 같은 의미의 조건이나 서비스별 유사 처리는 하나의 bullet로 합치세요.
6. 질문과 직접 관련 없는 비용, 광고, 일반 안내, 배경 설명은 참고 문서에 있어도 제외하세요.
7. "문서에서 확인되지 않습니다", "확인되지 않은 항목" 같은 미확인 문장은 쓰지 마세요.
8. 마지막 줄에 "근거: 문서명1, 문서명2" 형식으로 가장 중요한 출처명을 최대 3개만 적으세요.
9. 근거에는 참고 문서의 "출처:" 뒤에 있는 실제 문서명만 그대로 쓰고, "문서1", "문서2", "[1]" 같은 번호 별칭은 쓰지 마세요.
10. 원문을 길게 인용하거나 같은 내용을 반복하지 마세요.

[참고 문서]
{context}

[질문]
{question}

[답변]"""


CONCISE_SUMMARY_TEMPLATE = """당신은 주어진 참고 문서만 근거로 답변하는 한국어 지식 어시스턴트입니다.

답변 규칙:
1. 반드시 한국어로 답변하세요.
2. 문서에 있는 내용만 근거로 사용하고 문서 밖 추론은 하지 마세요.
3. 답변은 "요약"과 "근거" 두 부분만 작성하세요.
4. "요약"은 최대 4문장으로 질문의 핵심 답만 작성하세요.
5. "근거"는 사용한 출처 문서명만 쉼표로 나열하세요.
6. 문서에서 확인되지 않는 항목은 요약 안에 "문서에서 확인되지 않습니다"라고 명시하세요.
7. 조항 전체를 길게 풀어쓰거나 중복 설명하지 마세요.

[참고 문서]
{context}

[질문]
{question}

[답변]"""


@dataclass(frozen=True)
class Case:
    case_id: str
    question: str
    doc_type: str | None = None


CASES = [
    Case(
        case_id="long_general",
        question="서비스 해지 시 데이터 및 게시물은 어떻게 처리되는가?",
    ),
    Case(
        case_id="location_purpose",
        question="위치기반서비스 약관에서 개인위치정보는 어떤 목적으로 이용되는가?",
        doc_type="위치기반서비스",
    ),
    Case(
        case_id="operation_limit",
        question="운영정책에서 계정 이용이 제한되거나 해지될 수 있는 조건은 무엇인가?",
        doc_type="운영정책",
    ),
]


def main() -> int:
    baseline_template = engine_mod.PROMPT_TEMPLATE
    templates = [
        ("baseline", baseline_template),
        ("concise_bullet", CONCISE_BULLET_TEMPLATE),
        ("refined_concise_bullet", REFINED_CONCISE_BULLET_TEMPLATE),
        ("concise_summary", CONCISE_SUMMARY_TEMPLATE),
    ]
    template_filter = {
        name.strip()
        for name in os.environ.get("TEMPLATE_FILTER", "").split(",")
        if name.strip()
    }
    if template_filter:
        templates = [(name, template) for name, template in templates if name in template_filter]
        missing_templates = template_filter - {name for name, _template in templates}
        if missing_templates:
            raise ValueError(f"unknown template filter: {sorted(missing_templates)}")

    vector_store = VectorStore(db_path="./chroma_db", collection_name="ragSystem")
    embedder = EmbeddingEngine()
    llm = OllamaLLM(model="gemma3:12b")
    rag = RAGEngine(vector_store=vector_store, embedding_engine=embedder, llm=llm)

    results = []
    try:
        rag.query(
            "서비스 해지 시 데이터는 어떻게 처리되는가?",
            trace_route="concise.prompt.experiment.warmup",
            trace_metadata={"case_id": "warmup", "template": "baseline"},
        )
        for case in CASES:
            for template_name, template in templates:
                engine_mod.PROMPT_TEMPLATE = template
                start = time.perf_counter()
                try:
                    result = rag.query(
                        case.question,
                        doc_type=case.doc_type,
                        trace_route="concise.prompt.experiment",
                        trace_metadata={
                            "case_id": case.case_id,
                            "template": template_name,
                        },
                    )
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    row = {
                        "case_id": case.case_id,
                        "template": template_name,
                        "elapsed_ms": round(elapsed_ms, 2),
                        "answer_length": len(result["answer"]),
                        "sources": len(result["sources"]),
                        "answer_preview": result["answer"][:350].replace("\n", " / "),
                    }
                except Exception as e:
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    row = {
                        "case_id": case.case_id,
                        "template": template_name,
                        "elapsed_ms": round(elapsed_ms, 2),
                        "error": str(e),
                    }
                results.append(row)
                print(json.dumps(row, ensure_ascii=False), flush=True)
    finally:
        engine_mod.PROMPT_TEMPLATE = baseline_template

    print("SUMMARY_JSON=" + json.dumps(results, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
