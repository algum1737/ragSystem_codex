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

- 실제 Ubuntu 서버 systemd 환경에서의 trace 파일 생성 확인은 로컬 작업 범위를 넘어 다음 runtime verification plan으로 분리했다.

## Open Work

- 없음. 서버 적용/운영 로그 확인은 후속 작업으로 진행한다.

## Completion

- `observability.trace` 로컬 JSONL trace writer를 추가했다.
- `RAG_TRACE_ENABLED` opt-in, `RAG_TRACE_PATH`, `RAG_TRACE_INCLUDE_PREVIEW` 환경변수를 추가했다.
- API `/query`, CLI query, `RAGEngine.query()` 경계에서 route, trace id, model, top_k, retrieved source path, latency, answer length를 기록한다.
- eval pipeline에서 `eval.case` event로 `case_id`, model, top_k, retrieved sources, query latency, score를 기록한다.
- trace 출력 경로 `logs/`를 gitignore에 추가했다.
- 구현 결과를 `docs/references/2026-06-02-local-observability-trace-result.md`에 기록했다.

## Validation Result

- 통과: `bash scripts/validate-docs.sh`
- 통과: `.venv/bin/python -m py_compile api/main.py retriever/engine.py eval/pipeline.py query.py observability/trace.py`
- 통과: trace enabled local JSONL smoke
  - `question_hash`, `retrieved_sources`, `latency_ms`, `answer_length` 기록 확인
  - full answer, chunk text, `question_preview` 기본 미포함 확인
- 통과: trace disabled smoke
  - `RAG_TRACE_ENABLED=false`에서 trace file 미생성 확인
- 통과: eval trace smoke
  - `eval.case`, `eval_case_id`, `eval_scores`, `query_total` latency 기록 확인
