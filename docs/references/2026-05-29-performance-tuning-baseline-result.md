# 2026-05-29 Performance Tuning Baseline Result

## Purpose

성능 튜닝 전후를 같은 기준선으로 비교하고, 1차 튜닝 결과가 안정화 기준을 충족하는지 기록한다.

## Evaluation Environment

- 실행 위치: Ubuntu 서버 `/opt/ragSystem_codex`
- 평가 기준 모델: `gemma3:12b`
- 운영 기본 모델: `gemma4:26b`
- `top_k`: 5
- Chroma collection count: 318

## Baseline Before Tuning

- 리포트: `eval/results/eval_20260529_172801.json`
- `accuracy_mean=0.9565`
- `faithfulness_mean=0.913`
- `not_found_success_rate=0.0`
- 주요 실패:
  - `tc-16`: 답변은 미확인이라고 했지만 no-answer 탐지식이 `"찾을 수 없습니다"`만 인식해 실패했다.
  - `tc-18`: 답변 accuracy는 통과했지만 faithfulness judge가 실패했다.
  - `tc-17`: `rag_normalized_source_precision@k=0.75`, `source_recall@k=0.75`로 낮다.

## First Tuning Change

`eval/pipeline.py`의 no-answer 탐지식을 보강했다.

- 기존: `"찾을 수 없습니다"` 포함 여부만 확인
- 변경: 답변 전체가 아래 미확인 응답으로 시작하는 경우도 no-answer로 인식
  - `문서에서 확인되지 않는 내용입니다`
  - `제공된 문서에는`
  - `제공된 문서에서 확인되지 않습니다`

부분 답변의 하위 섹션에 포함된 `문서에서 확인되지 않는 내용`은 오탐하지 않도록 `startswith` 기준으로 제한했다.

## Result After Tuning

- 리포트: `eval/results/eval_20260529_173928.json`
- `accuracy_mean=1.0`
- `faithfulness_mean=0.9565`
- `not_found_rate=0.0435`
- `not_found_success_rate=1.0`
- `rag_normalized_source_precision@k_mean=0.9891`
- `source_recall@k_mean=0.9891`

## Stability Decision

현재 평가셋 기준 집계 지표는 안정화 기준을 통과하지만, source drift guard는 `tc-04` faithfulness를 critical로 분류한다. 따라서 완전 안정화 선언 전 잔여 케이스 리뷰가 필요하다.

- 통과: `accuracy_mean >= 0.95`
- 통과: `faithfulness_mean >= 0.95`
- 통과: `not_found_success_rate = 1.0`
- 미통과: source drift guard `--fail-on-critical`은 `tc-04` faithfulness 0.0 때문에 실패

## Residual Cases

- `tc-04`: faithfulness 0.0. source drift guard critical case이며, 답변 또는 judge context 선택을 별도 검토한다.
- `tc-17`: 검색 source recall 0.75. relevant source 범위 또는 검색 source diversity를 별도 검토한다.

## Next Candidate

다음 튜닝은 대규모 파라미터 변경보다 잔여 케이스 리뷰가 우선이다.
