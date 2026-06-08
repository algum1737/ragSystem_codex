# Gemma3 Token Cap Experiment Plan

## Goal

`gemma3:12b + top_k=5` 운영 조합에서 답변 길이 제한이 latency를 줄이면서 품질을 유지하는지 검증한다.

## Scope

- `gemma3:12b` 전용 `max_tokens` 또는 Ollama `num_predict` 제한 후보 정의
- 대표 query smoke로 latency와 빈 응답 여부 확인
- 필요 시 작은 케이스 subset으로 answer quality 회귀 확인
- 채택 여부 결정

## Out Of Scope

- `gemma4` 계열 token cap 적용
- `top_k` 변경
- systemd GPU 환경변수 변경
- full eval 즉시 실행

## Assumptions

- `gemma3:12b`는 이전 latency triage에서 `max_tokens` 제한이 정상 동작했다.
- `gemma4` 계열은 token cap 적용 시 빈 응답 리스크가 있어 이번 실험 대상이 아니다.
- 현재 운영 기본 모델은 `gemma3:12b`, 기본 `top_k`는 5다.

## Pre-flight checks

- 서버 `/health`가 `gemma3:12b`인지 확인
- 최근 post-transition trace 확인
- token cap 후보값을 사용자와 확정하거나 보수적으로 선택

## Steps

1. 후보 token cap 값을 정한다.
2. 대표 query 2-3건에서 capped/uncapped latency와 응답 품질을 비교한다.
3. 빈 응답, 과도한 답변 절단, source 누락이 있는지 확인한다.
4. 채택 여부와 구현 필요성을 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 `/query` 또는 CLI query smoke
- trace latency 확인
- 응답 preview 확인

## Skipped/Not Run

- full eval은 실행하지 않았다. 대표 질의 smoke에서 token cap 채택 불가 판단이 먼저 나왔다.
- `gemma4` 계열 token cap은 실행하지 않았다. 기존 빈 응답 리스크 때문에 범위 밖이다.

## Open Work

- 없음. token cap은 채택하지 않는다.
- 다음 active plan은 `docs/exec-plans/active/2026-06-05-gemma3-transition-wrapup.md`다.

## Completion

- `gemma3:12b + top_k=5` 운영 조합에서 `num_predict` 후보 128, 256, 384, 512, 768, 1024를 확인했다.
- 128은 운영정책 케이스에서 keyword accuracy가 회귀했다.
- 256, 384, 512는 하나 이상의 대표 질의에서 답변 절단 징후가 있었다.
- 768은 긴 해지/데이터 단건 직접 호출에서 완결됐지만, API 기본 cap으로 적용했을 때 같은 유형의 긴 답변이 불완전했다.
- 1024는 답변 완결성은 회복했지만 latency 개선이 실질적으로 없었다.
- 결론: 기본 token cap은 채택하지 않는다.
- 실험 중 반영했던 token cap 구현은 로컬과 서버에서 되돌렸다.
- 서버 API는 다시 token cap 없는 `gemma3:12b` 기본 모델 상태로 재시작했다.
- 결과 문서: `docs/references/2026-06-05-gemma3-token-cap-experiment-result.md`

## Validation Result

- 통과: pre-flight
  - 서버 `/health`: `{"status":"ok","model":"gemma3:12b"}`
  - 최근 post-transition trace 확인
- 통과: token cap smoke
  - 128/256/384/512/768/1024 후보 확인
  - 빈 응답은 없었다.
  - 128은 accuracy 회귀, 256/384/512/768은 절단 리스크, 1024는 latency 개선 부족으로 제외했다.
- 통과: rollback
  - 로컬 `retriever/llm.py`에서 기본 token cap 제거
  - 서버 `retriever/llm.py`에서도 기본 token cap 제거
  - 서버 compile 통과
  - 서버 API 재시작 후 `/health`: `{"status":"ok","model":"gemma3:12b"}`
  - 서버 확인: `DEFAULT_MODEL=gemma3:12b`, 기본 token cap 없음
- 통과: local compile
  - `.venv/bin/python -m py_compile retriever/llm.py query.py api/main.py app.py`
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
