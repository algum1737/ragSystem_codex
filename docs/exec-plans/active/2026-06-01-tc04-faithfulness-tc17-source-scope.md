# TC04 Faithfulness And TC17 Source Scope Plan

## Goal

잔여 critical/watch 후보인 `tc-04` faithfulness 실패와 `tc-17` source scope 불일치를 좁게 보정한다.

## Scope

- `tc-04` faithfulness judge 입력 context와 답변 citation 표현 진단
- `tc-04`에 대한 좁은 보정 후보 선정
- `tc-17` relevant source 범위 재검토
- 필요 시 평가셋 source scope 또는 평가 하네스 보정
- 보정 후 full eval과 source drift guard 실행

## Out Of Scope

- 운영 모델 변경
- 전역 프롬프트 대규모 변경
- 검색 파라미터 전체 튜닝
- GPU/서버 런타임 변경

## Assumptions

- `eval/results/eval_20260529_173928.json`이 현재 채택 기준 리포트다.
- 2026-06-01 전역 출처 프롬프트 실험은 full eval 회귀가 있어 채택하지 않는다.
- `tc-17`은 답변 품질 문제가 아니라 source scope 문제일 가능성이 높다.

## Pre-flight checks

- `git status --short --branch` 확인
- `eval/results/eval_20260529_173928.json` 확인
- `docs/references/2026-06-01-residual-tuning-case-review.md` 확인

## Steps

1. `tc-04` faithfulness judge prompt와 selected contexts를 재현한다.
2. `tc-04` 보정 후보를 전역 회귀가 적은 방식으로 좁힌다.
3. `tc-17` relevant source 범위를 source scope policy 기준으로 재검토한다.
4. 필요한 최소 변경만 적용한다.
5. full eval과 source drift guard로 회귀 여부를 확인한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py`
- `.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5`
- `.venv/bin/python scripts/source_drift_report.py <latest-report> --fail-on-critical`

## Manual/Runtime QA

- `tc-04`, `tc-17` 답변과 검색 source를 사람이 검토한다.

## Skipped/Not Run

- 아직 보정 구현과 재평가는 실행하지 않았다.

## Open Work

- `tc-04` faithfulness diagnostic과 `tc-17` source scope calibration.
