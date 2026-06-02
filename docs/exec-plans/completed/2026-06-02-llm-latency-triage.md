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

- 대규모 full eval은 실행하지 않았다. 모델 전환 후보가 정해진 뒤 별도 plan에서 수행한다.

## Open Work

- 없음. 다음 작업은 운영 모델 전환 실험과 품질 재검증이다.

## Progress

- 운영 `rag_traces.jsonl` latency sample 확인.
- `ollama ps`, `nvidia-smi`, `ollama list` 확인.
- Ollama 단독 generate smoke 실행.
- RAG 유사 긴 context generate smoke 실행.
- 앱과 같은 LangChain `OllamaLLM.predict()` 경로에서 `max_tokens` 유무 비교.
- 서버 CLI RAG 경로에서 `gemma3:12b` trace smoke 실행.
- 분석 결과 기록: `docs/references/2026-06-02-llm-latency-triage-result.md`

## Validation Result

- 통과: 운영 trace sample 확인
  - `gemma4:26b` API trace total 약 217.8초, LLM 약 207.9초
- 통과: GPU/Ollama 상태 확인
  - `gemma4:26b`는 `15%/85% CPU/GPU`로 일부 CPU offload 발생
- 통과: Ollama 단독 generate smoke
  - 짧은 prompt와 긴 context에서 모델별 timing 확인
- 통과: LangChain 경로 max token 비교
  - `gemma4:26b`는 `max_tokens` 적용 시 빈 응답 리스크 확인
  - `gemma3:12b`는 `max_tokens` 적용 정상
- 통과: `gemma3:12b` CLI RAG trace smoke
  - total 약 26.3초, LLM 약 16.5초

## Completion

- LLM 지연의 주 병목이 retrieval이 아니라 `gemma4:26b` LLM 생성 구간임을 확인했다.
- 1차 개선 후보를 `gemma3:12b` 운영 모델 전환 실험으로 정했다.
