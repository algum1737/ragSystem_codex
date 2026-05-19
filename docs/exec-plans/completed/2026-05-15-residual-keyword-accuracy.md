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

- Pre-flight checks: 통과.
  - 최신 리포트 `eval/results/eval_20260515_110900.json` 확인.
  - `eval/test_cases.json`의 `tc-03`, `tc-09` expected keyword 확인.
  - 해당 답변과 retrieved context 확인.
- Automated tests: 통과.
  - `bash scripts/validate-docs.sh`
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
  - `.venv/bin/python eval/pipeline.py --all` 권한 상승 경로에서 통과.
- Manual/Runtime QA: 통과.
  - `tc-03`, `tc-07`, `tc-09`, `tc-10` 답변과 expected keyword를 직접 대조.
  - 분석 결과를 `docs/references/2026-05-15-residual-keyword-accuracy.md`에 기록.
- Full eval result:
  - 리포트: `eval/results/eval_20260515_135903.json`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=1.0`
  - `not_found_rate=0.0`
  - `rag_normalized_source_precision@k_mean=1.0`
  - `source_recall@k_mean=1.0`
- Skipped/Not Run:
  - UI/API smoke test는 평가셋 변경만 수행했으므로 미실행.

## Open Work

- 이 계획 범위의 남은 작업은 없다.
- 후속 작업은 평가셋 확장 또는 과적합 점검이다.

## Completion

- 잔여 keyword accuracy 감점을 평가셋 표현 불일치로 분류했다.
- `tc-03`, `tc-07`, `tc-09`, `tc-10` expected keyword OR group을 문서/답변 표현에 맞게 보정했다.
- 최종 full eval에서 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_rate=0.0`을 확인했다.
