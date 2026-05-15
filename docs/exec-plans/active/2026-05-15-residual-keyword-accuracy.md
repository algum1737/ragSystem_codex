# Residual Keyword Accuracy Plan

## Goal

faithfulness 안정화 이후 남은 `tc-03`, `tc-09` keyword accuracy 감점 원인을 분리하고 다음 개선 후보를 정한다.

## Scope

- 최신 리포트 `eval/results/eval_20260515_110900.json` 기준 `tc-03`, `tc-09` 분석
- expected keyword와 실제 답변 표현 대조
- 평가셋 보정, 답변 형식 보정, no-op 후보 분리

## Out Of Scope

- 검색 튜닝
- faithfulness judge 변경
- 모델 교체
- 외부 API 평가 도입

## Assumptions

- 최신 full eval에서 `faithfulness_mean=1.0`, `not_found_rate=0.0`이다.
- 남은 accuracy 감점은 답변 근거 부족보다 keyword exact-match 표현 불일치일 가능성이 높다.

## Pre-flight checks

- 최신 리포트 `eval/results/eval_20260515_110900.json` 확인
- `eval/test_cases.json`의 `tc-03`, `tc-09` expected keyword 확인
- 해당 답변과 retrieved context 확인

## Steps

1. `tc-03`, `tc-09`에서 누락된 keyword group을 추출한다.
2. 답변이 문서 근거에는 충실한지 확인한다.
3. expected keyword 보정 후보와 답변 형식 보정 후보를 분리한다.
4. 다음 작업을 구현 또는 no-op으로 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`

## Manual/Runtime QA

- `tc-03`, `tc-09` 답변과 expected keyword를 직접 대조한다.

## Skipped/Not Run

- 분석 계획이므로 full eval 재실행은 기본 검증에서 제외한다.

## Validation Result

- 아직 실행 전.

## Open Work

- `tc-03`, `tc-09` 잔여 keyword accuracy 분석
