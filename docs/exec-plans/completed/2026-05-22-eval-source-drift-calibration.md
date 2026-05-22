# Eval Source Drift Calibration Plan

## Goal

확장 corpus 기준으로 남은 `tc-04`, `tc-06` 실패를 정리해 평가셋 정의와 keyword 기준을 안정화한다.

## Scope

- `tc-04` 자동 갱신/해지 복합 질문 재정의
- `tc-06` 분쟁 해결 keyword 기준 보정 또는 케이스 분리
- full eval 재실행 및 결과 문서화

## Out Of Scope

- 검색 알고리즘 변경
- 모델 교체
- 신규 문서 인제스천

## Assumptions

- `expected_not_found` 정책은 `tc-16`에서 정상 동작한다.
- 다문서 faithfulness context는 5개 context 기준으로 `tc-09`, `tc-10` 회귀를 해소했다.
- 남은 주요 실패는 평가셋 정의와 source drift 성격이 강하다.

## Pre-flight checks

- `docs/references/2026-05-22-eval-failure-triage.md` 확인
- `eval/results/eval_20260522_131753.json` 확인
- `eval/test_cases.json`의 `tc-04`, `tc-06` 확인

## Steps

1. `tc-04`를 자동 갱신 negative case와 해지 방법 positive case로 분리할지 결정한다.
2. `tc-06` expected keyword group에 협의/소송/법원/제소 표현을 반영할지 검토한다.
3. 필요한 경우 `eval/test_cases.json`을 수정한다.
4. full eval을 재실행하고 결과를 기록한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- `.venv/bin/python eval/pipeline.py --all`

## Manual/Runtime QA

- 변경이 기존 hard case의 난도를 부당하게 낮추지 않는지 확인한다.
- `tc-04`, `tc-06` 답변과 retrieved source를 직접 대조한다.

## Skipped/Not Run

- 없음.

## Validation Result

- Pre-flight checks
  - `docs/references/2026-05-22-eval-failure-triage.md` 확인.
  - `eval/results/eval_20260522_131753.json` 확인.
  - `eval/test_cases.json`의 `tc-04`, `tc-06` 확인.
- Automated tests
  - `jq empty eval/test_cases.json` 통과.
  - `bash scripts/validate-docs.sh` 통과.
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py` 통과.
  - `.venv/bin/python eval/pipeline.py --all` 실행 완료.
    - 최종 리포트: `eval/results/eval_20260522_160844.json`
    - `total_cases=17`
    - `accuracy_mean=1.0`
    - `faithfulness_mean=1.0`
    - `not_found_rate=0.0588`
    - `not_found_success_rate=1.0`
- Manual/Runtime QA
  - `tc-04`는 유료서비스 자동 갱신 positive case로 통과.
  - `tc-06`은 협의/소송/법원/제소 표현을 반영해 통과.
  - `tc-16`은 expected no-answer negative case로 유지.
  - `tc-17`은 해지/개별 서비스 이용 종료 positive case로 통과.
  - 결과 문서: `docs/references/2026-05-22-eval-source-drift-calibration.md`

## Open Work

- 남은 작업 없음.
- 다음 후보: 신규 문서 추가 시 source drift를 자동 탐지하는 regression guard 또는 리포트 검토.
