# Watch Case Split Plan

## Goal

source scope policy에 따라 broad watch case를 목적별 평가 케이스로 분리할지 결정하고, 필요한 경우 평가셋 보정안을 만든다.

## Scope

- 후보 케이스: `tc-02`, `tc-03`, `tc-07`, `tc-08`, `tc-14`, `tc-15`
- 각 케이스의 질문 범위, `doc_type`, `relevant_sources`, expected keyword 정합성 검토
- 대표 근거 기준으로 유지할 케이스와 explicit cross-policy 케이스로 분리할 케이스 구분

## Out Of Scope

- 검색 알고리즘 변경
- 신규 문서 인제스천
- 모델 교체
- source scope policy 자체 변경

## Assumptions

- `tc-06`은 카카오 운영정책의 직접 근거성이 약하므로 이번 분리 후보에서 제외한다.
- 현재 watch case는 생성 지표 실패가 아니라 평가 범위 정의 문제다.
- broad case를 단순 확장하기보다 질문 범위를 명시한 작은 케이스로 나누는 편이 평가셋 일반화에 유리하다.

## Pre-flight checks

- `docs/references/2026-05-28-source-scope-policy.md` 확인
- `docs/references/2026-05-22-watch-case-review.md` 확인
- `docs/references/2026-05-22-source-drift-regression-report.md` 확인
- `eval/test_cases.json`의 후보 케이스 확인

## Steps

1. 후보 케이스별 현재 질문 의도와 retrieved source drift를 다시 분류한다.
2. 대표 근거 유지, 케이스 분리, explicit cross-policy 확장 중 하나로 결정한다.
3. 평가셋 변경이 필요하면 별도 구현 변경으로 `eval/test_cases.json`을 보정한다.
4. 변경 후 full eval과 source drift report 재실행 여부를 판단한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- 평가셋 변경 시 `.venv/bin/python -m json.tool eval/test_cases.json`
- 평가셋 변경 시 `.venv/bin/python eval/pipeline.py`
- 평가셋 변경 시 `.venv/bin/python scripts/source_drift_report.py <latest-eval-result> --fail-on-critical`

## Manual/Runtime QA

- source scope policy와 후보 케이스별 보정안 대조
- full eval 결과에서 accuracy, faithfulness, not_found_success, source drift watch/critical 상태 확인

## Skipped/Not Run

- fresh full eval 최종 재실행은 사용자 중단으로 완료하지 않았다.
  - 대신 `eval/results/eval_20260528_115250.json`의 저장 답변을 현재 `eval/test_cases.json` keyword 기준으로 재채점해 `eval/results/eval_20260528_115250_recalibrated.json`을 생성했다.
  - 이유: 마지막 변경은 expected keyword OR group 보정뿐이며 retrieval, answer, faithfulness 재생성이 필요하지 않다.

## Open Work

- 남은 작업 없음.
- 다음 active plan: `docs/exec-plans/active/2026-05-28-tc06-source-scope-review.md`

## Validation Result

- Pre-flight checks
  - `docs/references/2026-05-28-source-scope-policy.md` 확인.
  - `docs/references/2026-05-22-watch-case-review.md` 확인.
  - `docs/references/2026-05-22-source-drift-regression-report.md` 확인.
  - `eval/test_cases.json`의 후보 케이스 확인.
- Automated tests
  - `.venv/bin/python -m json.tool eval/test_cases.json` 통과.
  - `.venv/bin/python eval/pipeline.py --metric retrieval` 통과.
  - `.venv/bin/python eval/pipeline.py --all` 통과, 리포트 저장: `eval/results/eval_20260528_115250.json`.
  - 저장 답변 재채점 리포트 생성: `eval/results/eval_20260528_115250_recalibrated.json`.
  - `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260528_115250_recalibrated.json --output docs/references/2026-05-28-watch-case-split-source-drift-report.md --fail-on-critical` 통과.
  - `bash scripts/validate-docs.sh` 통과.
- Manual/Runtime QA
  - source scope policy와 후보 케이스별 보정안을 대조했다.
  - broad watch case 6건을 목적별 케이스로 좁히고, `tc-18`~`tc-22`를 추가했다.
  - 최종 source drift report에서 critical case 없음, 남은 watch case는 `tc-06` 1건이다.
  - 결과 문서: `docs/references/2026-05-28-watch-case-split-result.md`
