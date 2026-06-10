# Concise Lightweight Eval Harness Plan

## Goal

문서로 정의한 concise mode 경량 평가셋을 실행 가능한 eval harness로 반영한다.

## Scope

- `eval/concise_test_cases.json` 추가
- required point, forbidden claim, answer length, source count 기반 deterministic 판정 구현
- `answer_mode=concise` 경로로만 실행되는 smoke/eval 명령 추가
- trace metadata와 결과 JSON에 `answer_mode=concise`를 남기는지 확인

## Out Of Scope

- 운영 기본 answer mode 변경
- 자동 라우팅 구현
- standard full eval 기준 변경
- 프롬프트 변경

## Assumptions

- 사용자 승인 후에만 구현 변경을 진행한다.
- 경량셋 정의는 `docs/references/2026-06-10-concise-lightweight-eval-set.md`를 기준으로 한다.
- 경량셋은 full eval을 대체하지 않는다.

## Pre-flight checks

- `git status --short --branch`
- `docs/references/2026-06-10-concise-lightweight-eval-set.md` 확인
- 구현 승인 여부 확인

## Steps

1. 평가셋 JSON 구조를 추가한다.
2. concise 전용 평가 실행 경로를 구현한다.
3. deterministic 판정 결과와 trace 정보를 결과 JSON에 기록한다.
4. 로컬 또는 서버에서 대표 smoke를 실행한다.
5. 구현 결과와 검증 결과를 문서화한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py query.py app.py`
- concise lightweight eval smoke 명령

## Manual/Runtime QA

- 필요 시 운영 또는 로컬 API에서 `answer_mode=concise` 대표 질의 1건 확인

## Skipped/Not Run

- full eval은 기본적으로 실행하지 않는다. standard 경로 변경이 생기면 별도 실행한다.

## Open Work

- 사용자 구현 승인
- concise lightweight eval harness 구현
