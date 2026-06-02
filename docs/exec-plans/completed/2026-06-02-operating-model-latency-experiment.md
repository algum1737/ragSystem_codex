# Operating Model Latency Experiment Plan

## Goal

운영 기본 모델을 `gemma3:12b`로 전환할지 판단하기 위해 latency와 품질을 함께 검증한다.

## Scope

- `gemma3:12b` 운영 API query smoke
- trace latency 확인
- 기존 eval 기준선과 비교 가능한 full eval 재실행
- 운영 기본 모델 변경 후보 문서화

## Out Of Scope

- 즉시 영구 전환
- GPU driver 변경
- Langfuse 연동
- UI 변경

## Assumptions

- `gemma3:12b`는 서버에 이미 설치되어 있다.
- `gemma3:12b` RAG CLI smoke는 total 약 26.3초, LLM 약 16.5초였다.
- 모델 변경은 품질 기준선을 통과해야 운영 기본값으로 반영한다.

## Pre-flight checks

- 운영 API 현재 model 확인
- `gemma3:12b` Ollama availability 확인
- trace file 활성화 상태 확인
- 최신 eval 기준선 확인

## Steps

1. API model change endpoint로 임시 `gemma3:12b` 전환을 검증한다.
2. 운영 API query trace latency를 확인한다.
3. full eval을 `gemma3:12b` 기준으로 실행한다.
4. latency와 품질 지표를 비교해 운영 기본 모델 변경 여부를 결정한다.
5. 필요 시 변경 plan을 별도로 만든다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 `/health` model 확인
- API `/query` trace 확인
- eval report 확인

## Skipped/Not Run

- 운영 기본 모델 영구 전환은 하지 않았다. 품질 기준선이 완전히 유지되지 않았기 때문이다.

## Open Work

- 없음. 다음 작업은 `gemma3:12b` 품질 gap 리뷰다.

## Progress

- `/model` endpoint가 실제 `RAGEngine._llm`을 바꾸지 못할 수 있는 버그를 확인했다.
- `RAGEngine.llm` property getter/setter를 추가해 model change endpoint가 실제 RAG query 모델을 바꾸도록 수정했다.
- 서버에 수정 파일을 반영하고 API를 재기동했다.
- API model change endpoint로 `gemma3:12b` 임시 전환을 확인했다.
- 운영 API query trace에서 `gemma3:12b` latency를 측정했다.
- `gemma3:12b` full eval을 실행하고 report를 로컬 저장소로 복사했다.
- 실험 후 운영 API 모델을 `gemma4:26b`로 복구했다.
- 결과 문서: `docs/references/2026-06-02-operating-model-latency-experiment-result.md`

## Validation Result

- 통과: local compile
  - `.venv/bin/python -m py_compile api/main.py retriever/engine.py`
- 통과: server compile
  - `.venv/bin/python -m py_compile retriever/engine.py api/main.py`
- 통과: API model change smoke
  - `gemma4:26b` → `gemma3:12b`
  - `/health` model `gemma3:12b`
- 통과: API query trace
  - model `gemma3:12b`
  - total 약 29.0초, LLM 약 19.2초
- 통과: full eval 실행
  - report `eval/results/eval_20260602_131307.json`
  - `accuracy_mean=0.9891`
  - `faithfulness_mean=0.9565`
  - `not_found_success_rate=1.0`
- 통과: 운영 API 모델 복구
  - `gemma3:12b` → `gemma4:26b`
  - `/health` model `gemma4:26b`

## Completion

- `gemma3:12b`가 latency를 크게 줄이는 것은 확인했다.
- 품질 기준선이 완전히 유지되지 않아 즉시 영구 전환은 보류한다.
- 다음 작업은 `tc-07`, `tc-11` 품질 gap 리뷰다.
