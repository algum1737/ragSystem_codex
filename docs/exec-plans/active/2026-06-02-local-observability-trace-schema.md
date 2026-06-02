# Local Observability Trace Schema Plan

## Goal

Langfuse 도입 전 단계로 privacy-safe local trace sink를 추가해 운영 query와 eval case를 재현 가능한 형태로 추적한다.

## Scope

- 로컬 JSONL trace event 스키마 구현
- `RAG_TRACE_ENABLED` 환경변수로 opt-in 활성화
- API `/query`와 `RAGEngine.query()` 또는 인접 경계에 trace id와 latency 기록
- eval case 실행 시 `case_id`, model, top_k, scores 연결
- full prompt, full answer, chunk text는 기본 비저장

## Out Of Scope

- Langfuse Cloud 연동
- 외부 데이터 전송
- self-hosted Langfuse 배포
- Streamlit UI 변경

## Assumptions

- 현재 운영 서버는 내부망이며 질의/문서/답변은 민감 데이터일 수 있다.
- 관측 기능은 기본 off로 둔다.
- trace sink는 장애가 나도 RAG query를 실패시키면 안 된다.

## Pre-flight checks

- `api/main.py` query boundary 확인
- `retriever/engine.py` query/retrieve/LLM call boundary 확인
- `eval/pipeline.py` case loop 확인
- `logs/` 또는 trace output 경로의 gitignore 상태 확인

## Steps

1. trace event schema와 writer를 추가한다.
2. RAG query 경계에 total latency와 retrieved source 기록을 추가한다.
3. eval pipeline에 case id와 scores 기록을 연결한다.
4. trace disabled 상태에서 기존 동작이 변하지 않는지 확인한다.
5. trace enabled smoke test로 JSONL 1건 이상을 확인한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile api/main.py retriever/engine.py eval/pipeline.py`
- trace disabled query/eval smoke
- trace enabled local JSONL smoke

## Manual/Runtime QA

- trace payload에 full prompt, full answer, chunk text가 기본 포함되지 않는지 확인한다.

## Skipped/Not Run

- 아직 구현은 수행하지 않았다.

## Open Work

- local trace sink 구현.
