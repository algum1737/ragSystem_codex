# 2026-06-02 Observability And Langfuse Review

## Purpose

현재 자체 eval/log 기반 운영 방식에 Langfuse 같은 LLM observability 도구를 도입할지 검토하고, 도입한다면 최소 범위를 정한다.

## Current State

현재 프로젝트에는 Langfuse 또는 유사 LLM observability 도구가 연동되어 있지 않다.

현재 관측 수단:

- FastAPI/systemd 로그
- `retriever.engine`의 RAG query 로그
- `eval/results/*.json` full eval 리포트
- `scripts/source_drift_report.py` source drift guard
- 수동 서버 검증: `/health`, `/stats`, Streamlit HTTP, 실제 query

부족한 항목:

- 운영 query 단위 trace id
- query별 latency 분해: embedding, retrieval, rerank, prompt build, LLM
- retrieved source와 answer의 쌍 저장
- 운영 query와 eval score의 연결
- 실패 query 재현용 최소 메타데이터

## Langfuse Facts From Official Docs

Langfuse는 LLM observability, prompt management, evaluation, metrics를 제공하는 open-source LLM engineering platform이다.

공식 문서 기준:

- Python SDK와 JS/TS SDK를 제공하고, 다른 언어는 OpenTelemetry endpoint로 instrument할 수 있다.
- 최신 SDK는 OpenTelemetry 기반이며 spans/generations/events를 Langfuse observations로 변환한다.
- OTLP endpoint는 `/api/public/otel`이며 local/self-hosted endpoint도 사용할 수 있다.
- Langfuse Cloud 외에 self-hosted OSS와 self-hosted Enterprise 옵션이 있다.
- Self-hosted는 자체 인프라에 배포할 수 있고, 공식 security 문서는 self-hosted가 offline/air-gapped로도 실행 가능하다고 설명한다.
- OpenTelemetry baggage는 service boundary와 third-party API로 전파될 수 있으므로 password, API key, personal data 같은 민감 정보를 넣지 않아야 한다.

References:

- https://langfuse.com/docs/observability/sdk/overview
- https://langfuse.com/integrations/native/opentelemetry
- https://langfuse.com/security

## Security Review

현재 보안 기준은 외부 LLM API 대신 Ollama 로컬 모델을 쓰고, 문서 원문과 생성 결과를 로컬 환경에서 다루는 것이다.

따라서 외부 SaaS Langfuse Cloud를 즉시 붙이는 것은 현재 운영 기준과 맞지 않는다. 약관 문서 청크, 사용자 질의, 답변, 출처 문서명이 trace payload에 포함될 수 있기 때문이다.

허용 가능한 순서:

1. 로컬 JSONL trace sink 도입
2. trace payload redaction 기준 고정
3. self-hosted Langfuse를 내부망에 띄울 수 있는지 검토
4. 필요할 때만 Langfuse exporter를 optional backend로 추가

## Proposed Trace Schema

최소 trace event는 아래 필드로 시작한다.

- `trace_id`
- `timestamp`
- `route`: `api.query`, `eval.case`, `cli.query`
- `question_hash`
- `question_preview`: 길이 제한, 선택적 저장
- `doc_type`
- `model`
- `top_k`
- `retrieved_sources`: source path만, chunk text는 기본 비저장
- `latency_ms.total`
- `latency_ms.embedding`
- `latency_ms.retrieval`
- `latency_ms.rerank`
- `latency_ms.llm`
- `answer_length`
- `error_type`
- `eval_case_id`: eval 실행 시만
- `eval_scores`: eval 실행 시만

기본값은 chunk text, full prompt, full answer를 저장하지 않는다. 디버그 모드에서만 별도 환경변수로 허용한다.

## Decision

Langfuse 자체는 이 프로젝트의 RAG 운영과 튜닝에 유용하다. 다만 현재 단계에서 바로 외부 SaaS에 붙이지 않는다.

결정:

- 즉시 Langfuse Cloud 연동은 보류한다.
- 먼저 privacy-safe local trace sink를 구현한다.
- Langfuse는 self-hosted 또는 internal-only exporter 후보로 유지한다.
- 구현은 dependency를 필수로 추가하지 않고 optional adapter 형태로 설계한다.

## First Implementation Candidate

다음 작업에서는 Langfuse SDK를 바로 추가하지 않고 로컬 관측 기반을 먼저 만든다.

- `observability/trace.py` 추가
- `RAG_TRACE_ENABLED=true`일 때만 JSONL trace 기록
- 기본 trace path: `./logs/rag_traces.jsonl`
- API query와 eval case에 `trace_id` 부여
- source path, latency, model, top_k 기록
- full prompt/answer/chunk text는 기본 비저장

이후 self-hosted Langfuse가 준비되면 같은 trace event를 Langfuse span/generation으로 내보내는 adapter를 추가한다.
