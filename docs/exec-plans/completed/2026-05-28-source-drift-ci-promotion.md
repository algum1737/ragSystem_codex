# Source Drift CI Promotion Plan

## Goal

source drift report를 CI 또는 정적 검증 루프에 승격할지 검토한다.

## Scope

- 현재 source drift report가 critical/watch case 없이 안정화된 상태인지 확인
- `scripts/source_drift_report.py`를 CI에 포함할 기준 검토
- full eval 결과 JSON 의존성을 CI에서 어떻게 다룰지 결정

## Out Of Scope

- 검색 알고리즘 변경
- 신규 평가 케이스 추가
- 모델 교체
- 즉시 full eval 자동화

## Assumptions

- 최신 평가셋은 23개 케이스다.
- 최신 source drift report 기준 critical/watch case는 없다.
- CI에서 LLM full eval을 직접 실행하기보다는 저장 리포트 기반 guard를 우선 검토한다.

## Pre-flight checks

- `docs/references/2026-05-28-location-dispute-case-review.md` 확인
- `docs/references/2026-05-28-location-dispute-case-report.md` 확인
- `.github/workflows/`의 현재 static checks 확인
- `scripts/source_drift_report.py` 사용 방식 확인

## Steps

1. 현재 CI가 실행하는 검증 범위를 확인한다.
2. source drift guard를 저장 리포트 기반으로 추가할 수 있는지 검토한다.
3. CI 승격이 부적절하면 로컬 검증 스크립트 후보로 문서화한다.
4. 필요 시 별도 구현 변경을 수행한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- CI 변경 시 관련 workflow 문법 확인

## Manual/Runtime QA

- CI에서 네트워크/로컬 모델 의존 없이 실행 가능한지 검토

## Skipped/Not Run

- full eval 재실행은 수행하지 않는다. 이 작업은 저장된 최신 eval 결과를 CI guard로 승격하는 범위다.

## Completion

- `.github/workflows/ci.yml`에 저장 리포트 기반 source drift guard를 추가했다.
- CI는 `eval/results/eval_20260528_115250_location_dispute_added.json`을 입력으로 `scripts/source_drift_report.py --fail-on-critical`을 실행한다.
- 최신 source drift report는 critical/watch case가 없으므로 CI 실패 조건으로 사용 가능하다고 판단했다.

## Validation Result

- 통과: `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260528_115250_location_dispute_added.json --fail-on-critical`
- 통과: `python3 scripts/source_drift_report.py eval/results/eval_20260528_115250_location_dispute_added.json --fail-on-critical`
- 통과: `bash scripts/validate-docs.sh`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py scripts/source_drift_report.py ingestion/embedder.py ingestion/vector_store.py`

## Open Work

- 없음.
