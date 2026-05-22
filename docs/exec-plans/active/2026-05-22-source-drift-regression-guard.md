# Source Drift Regression Guard Plan

## Goal

신규 문서 추가 또는 평가셋 확장 후 source drift를 자동으로 발견할 수 있는 regression guard 후보를 검토한다.

## Scope

- 최신 source drift calibration 결과 검토
- 기존 eval result JSON에서 drift 후보를 판별할 수 있는 신호 검토
- guard를 스크립트, 리포트, CI 후보 중 어디에 둘지 결정

## Out Of Scope

- 신규 평가 케이스 추가
- 검색 알고리즘 변경
- 모델 교체
- CI workflow 즉시 변경

## Assumptions

- 최신 full eval 기준 생성 지표는 `accuracy_mean=1.0`, `faithfulness_mean=1.0`이다.
- 다음 위험은 현재 케이스의 점수 하락보다 신규 corpus 반영 시 `relevant_sources`와 실제 retrieved source가 어긋나는 drift다.
- guard는 먼저 리포트 또는 로컬 스크립트 후보로 설계하고, CI 승격은 별도 판단한다.

## Pre-flight checks

- `docs/references/2026-05-22-eval-source-drift-calibration.md` 확인
- `eval/results/eval_20260522_160844.json` 확인
- `eval/test_cases.json`의 `relevant_sources` 구조 확인

## Steps

1. source drift를 판별할 수 있는 기존 지표를 정리한다.
2. 신규 guard가 필요한지, 기존 eval summary로 충분한지 판단한다.
3. 구현한다면 리포트 전용 스크립트와 CI guard 중 우선순위를 정한다.
4. 필요한 경우 별도 구현 active plan을 만든다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 최신 eval 결과에서 `tc-04`, `tc-06`, `tc-16`, `tc-17`의 source alignment를 대조한다.

## Skipped/Not Run

- 아직 실행 전.

## Validation Result

- 아직 실행 전.

## Open Work

- source drift regression guard 설계 검토 진행.
