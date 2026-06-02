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

- 아직 실험 전이다.

## Open Work

- `gemma3:12b` API 임시 전환 smoke.
- full eval 재검증.
