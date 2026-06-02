# LLM Latency Triage Plan

## Goal

운영 trace에서 확인된 `gemma4:26b` LLM 생성 지연을 분류하고, 성능 튜닝 후보를 정한다.

## Scope

- trace latency에서 retrieval과 LLM 생성 시간을 분리한다.
- Ollama 모델별 응답 시간을 비교할 후보를 정한다.
- 프롬프트/context 길이와 `max_context_chars`, top_k 영향도를 확인한다.
- 운영 기본 모델 변경 여부는 판단 후보로만 남긴다.

## Out Of Scope

- 즉시 모델 교체
- GPU driver 변경
- Langfuse 도입
- 대규모 eval 재실행

## Assumptions

- 운영 trace 기준 검색/임베딩/rerank는 약 10초 내외다.
- `gemma4:26b` LLM 생성은 208초에서 351초까지 관측됐다.
- 모델 변경은 품질 기준선을 재확인한 뒤 결정해야 한다.

## Pre-flight checks

- 최신 trace file 확인
- Ollama 모델 목록 확인
- 현재 API 기본 모델 확인
- 기존 평가 기준 모델과 운영 모델 분리 정책 확인

## Steps

1. 최근 trace latency 샘플을 요약한다.
2. Ollama 단독 generate 속도와 RAG query 속도를 분리한다.
3. `gemma3:12b` 등 기존 보유 모델과 비교 후보를 정한다.
4. latency 개선 후보와 품질 재검증 계약을 정리한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 `rag_traces.jsonl` latency sample 확인
- Ollama 단독 prompt smoke

## Skipped/Not Run

- 아직 분석 전이다.

## Open Work

- LLM latency sample 분석.
- 모델/프롬프트/context 튜닝 후보 정리.
