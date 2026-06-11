# Concise 06 Stability Fix Plan

## Goal

`concise-06`가 통지 방법과 사전/사후 예외를 안정적으로 보존하도록 평가 rule과 concise prompt 보강 후보를 좁게 적용하고 검증한다.

## Scope

- `concise-06` deterministic rule의 동의 표현 허용 범위 보정
- `CONCISE_PROMPT_TEMPLATE`의 조건/예외 보존 규칙 후보 검토
- 로컬 정적 검증
- 서버 `concise-06` 반복 smoke
- 서버 concise lightweight eval smoke

## Out Of Scope

- 운영 기본 answer mode 변경
- 자동 라우팅 구현
- standard prompt 변경
- full eval 실행
- 검색 인덱스 재구축

## Assumptions

- `concise-06` 검색 top-5에는 사전/사후 예외 근거가 포함된다.
- 통지 방법 세부 청크는 벡터스토어에 있으나 원 질문 top-5에 항상 직접 포함되지는 않는다.
- concise 답변은 700자 이하를 유지해야 한다.
- 구현 변경은 사용자 승인 후 진행한다.

## Pre-flight checks

- `git status --short --branch`
- `docs/references/2026-06-11-concise-06-failure-triage-result.md` 확인
- `eval/concise_test_cases.json`의 `concise-06` rule 확인
- `retriever/engine.py`의 `CONCISE_PROMPT_TEMPLATE` 확인

## Steps

1. `concise-06` rule에 필요한 동의 표현 후보를 최소 추가한다.
2. prompt 보강이 필요한지, rule 보정만으로 충분한지 먼저 판단한다.
3. prompt 보강을 적용한다면 조건/예외 질문에서 예외를 생략하지 않는 좁은 문장만 추가한다.
4. 로컬 정적 검증을 실행한다.
5. 서버에 변경분을 반영해 `concise-06` 반복 smoke를 실행한다.
6. 서버 concise lightweight eval smoke를 실행한다.
7. 결과를 문서화하고 plan을 완료 처리한다.

## Automated tests

- `python -m py_compile retriever/engine.py eval/pipeline.py`
- `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`
- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 `concise-06` 단일 질의 3회 이상 반복
- 서버 `bash scripts/run-concise-eval-smoke.sh`

## Skipped/Not Run

- full eval은 실행하지 않는다. 이 작업은 `concise` 전용 경량 회귀 보정이다.

## Open Work

- 사용자 승인 후 구현 변경 진행
