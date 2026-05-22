# Eval Generalization Review Plan

## Goal

현재 평가셋 기준 모든 주요 지표가 상한에 도달한 뒤, 평가셋이 과적합됐는지와 다음 확장 방향을 점검한다.

## Scope

- 최신 리포트 `eval/results/eval_20260515_135903.json` 기준 결과 해석
- 현재 10개 케이스의 범위와 한계 검토
- 다음 평가셋 확장 후보 선정

## Out Of Scope

- 검색 튜닝
- 프롬프트 변경
- 모델 교체
- 외부 API 평가 도입

## Assumptions

- 현재 평가셋에서는 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_rate=0.0`이다.
- 다음 개선은 기존 10개 케이스 점수 상승보다 평가셋 일반화가 우선이다.

## Pre-flight checks

- 최신 리포트 `eval/results/eval_20260515_135903.json` 확인
- `eval/test_cases.json` 전체 케이스 검토
- 최근 평가셋 보정 문서 확인

## Steps

1. 현재 10개 케이스의 질문 유형과 coverage를 분류한다.
2. keyword OR group이 과도하게 넓어진 케이스가 있는지 확인한다.
3. hard case 후보를 3개 이상 제안한다.
4. 다음 작업을 평가셋 확장, judge 개선, 또는 no-op으로 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`

## Manual/Runtime QA

- `eval/test_cases.json`의 질문/keyword/relevant_sources를 직접 검토한다.

## Skipped/Not Run

- 분석 계획이므로 full eval 재실행은 기본 검증에서 제외한다.

## Validation Result

- Pre-flight checks
  - `eval/results/eval_20260515_135903.json` 확인 완료.
  - `eval/test_cases.json` 10개 케이스 검토 완료.
  - `docs/references/2026-05-15-residual-keyword-accuracy.md` 확인 완료.
- Automated tests
  - `bash scripts/validate-docs.sh` 통과.
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py` 통과.
- Manual/Runtime QA
  - 현재 케이스 coverage와 keyword OR group 위험도를 `docs/references/2026-05-22-eval-generalization-review.md`에 기록.
  - hard case 후보 6개를 제안.
- Skipped/Not Run
  - full eval 재실행은 분석 계획 범위 밖이라 실행하지 않음.

## Open Work

- 남은 작업 없음.
- 다음 active plan: `docs/exec-plans/active/2026-05-22-eval-set-expansion.md`
