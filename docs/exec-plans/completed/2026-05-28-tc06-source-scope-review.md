# TC06 Source Scope Review Plan

## Goal

`tc-06` 분쟁 해결 케이스의 `relevant_sources` 범위를 source scope policy 기준으로 재검토한다.

## Scope

- `tc-06`의 질문 의도, expected keyword, retrieved source, source recall 대조
- 대표 근거 기준으로 좁힐지, explicit cross-policy 케이스로 유지할지 결정
- 필요한 경우 평가셋 보정 후보 작성

## Out Of Scope

- 검색 알고리즘 변경
- 신규 문서 인제스천
- 모델 교체
- 다른 watch case 재검토

## Assumptions

- `tc-06`은 최신 source drift report에서 남은 유일한 watch case다.
- 생성 지표는 `answer_accuracy=1.0`, `faithfulness=1.0`이므로 답변 품질 실패는 아니다.
- 현재 `relevant_sources`가 넓어 top-k source recall 해석이 흐려질 수 있다.

## Pre-flight checks

- `docs/references/2026-05-28-watch-case-split-result.md` 확인
- `docs/references/2026-05-28-watch-case-split-source-drift-report.md` 확인
- `eval/test_cases.json`의 `tc-06` 확인
- `eval/results/eval_20260528_115250_recalibrated.json` 확인

## Steps

1. `tc-06`의 현 `relevant_sources`를 대표 근거와 보조 근거로 분류한다.
2. 질문 문구가 전체 약관군 비교를 요구하는지 판단한다.
3. source scope policy에 따라 유지, 축소, 분리 중 하나를 선택한다.
4. 결정 내용을 문서화하고 필요한 경우 평가셋 변경 계획을 세운다.

## Automated tests

- `bash scripts/validate-docs.sh`
- 평가셋 변경 시 `.venv/bin/python -m json.tool eval/test_cases.json`
- 평가셋 변경 시 `.venv/bin/python eval/pipeline.py --metric retrieval`

## Manual/Runtime QA

- `tc-06` retrieved source와 답변 근거 대조
- source drift report에서 watch/critical 상태 확인

## Skipped/Not Run

- fresh full eval 재실행은 실행하지 않았다.
  - 이유: 변경은 `tc-06`의 `relevant_sources` 범위 축소뿐이며, 기존 저장 답변과 faithfulness를 재생성할 필요가 없다.
  - 대신 `eval/results/eval_20260528_115250_recalibrated.json`의 저장 retrieval/answer를 현재 평가셋 기준으로 재채점해 `eval/results/eval_20260528_115250_tc06_rescoped.json`을 생성했다.

## Open Work

- 남은 작업 없음.
- 다음 active plan: `docs/exec-plans/active/2026-05-28-location-dispute-case-review.md`

## Validation Result

- Pre-flight checks
  - `docs/references/2026-05-28-watch-case-split-result.md` 확인.
  - `docs/references/2026-05-28-watch-case-split-source-drift-report.md` 확인.
  - `eval/test_cases.json`의 `tc-06` 확인.
  - `eval/results/eval_20260528_115250_recalibrated.json` 확인.
- Automated tests
  - `.venv/bin/python -m json.tool eval/test_cases.json` 통과.
  - `.venv/bin/python eval/pipeline.py --metric retrieval` 통과.
  - `eval/results/eval_20260528_115250_tc06_rescoped.json` 생성.
  - `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260528_115250_tc06_rescoped.json --output docs/references/2026-05-28-tc06-source-scope-report.md --fail-on-critical` 통과.
  - `bash scripts/validate-docs.sh` 통과.
- Manual/Runtime QA
  - `tc-06`의 답변 근거를 retrieved source와 대조했다.
  - `tc-06`은 explicit cross-policy case가 아니라 대표 근거 회귀 케이스로 유지한다.
  - 위치기반서비스 분쟁 조정은 별도 hard case 후보로 분리한다.
  - 최종 source drift report 기준 critical/watch case 없음.
  - 결과 문서: `docs/references/2026-05-28-tc06-source-scope-review.md`
