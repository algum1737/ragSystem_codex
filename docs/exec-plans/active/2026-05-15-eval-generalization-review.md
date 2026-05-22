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

- 아직 실행 전.

## Open Work

- 평가셋 일반화 및 확장 방향 검토
