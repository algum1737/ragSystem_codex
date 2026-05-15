# Faithfulness Eval Stability Plan

## Goal

최신 평가에서 `tc-10` faithfulness 판정이 흔들리는 원인을 분리하고, 평가 프롬프트/컨텍스트/판정 방식 중 다음 개선 후보를 정한다.

## Scope

- `eval/results/eval_20260514_180006.json`의 `tc-10` 답변과 faithfulness 판정 검토
- faithfulness judge prompt가 답변의 부분 부정 문장을 과도하게 실패 처리하는지 확인
- full eval 반복 실행 없이 우선 판정 기준과 개선 후보를 분석

## Out Of Scope

- 검색 튜닝
- 답변 생성 프롬프트 대규모 변경
- 외부 API judge 도입
- 모델 교체

## Assumptions

- 최신 검색 지표는 source 기준 병목이 아니다.
- `tc-10` 답변은 주요 근거를 포함하지만, faithfulness judge가 부정 섹션 또는 컨텍스트 일부만 보고 실패 처리했을 가능성이 있다.

## Pre-flight checks

- 최신 유효 리포트 `eval/results/eval_20260514_180006.json` 확인
- `eval/pipeline.py`의 faithfulness prompt 확인
- `tc-10` retrieved context와 답변 직접 대조

## Steps

1. `tc-10` 답변과 context를 추출한다.
2. faithfulness judge가 본 `context_texts[:3]` 범위를 확인한다.
3. 답변의 어떤 문장이 근거 밖으로 판단될 수 있는지 분리한다.
4. 다음 후보를 평가 프롬프트 보정, context 범위 조정, 또는 no-op으로 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`

## Manual/Runtime QA

- `tc-10` 답변과 retrieved context를 직접 대조한다.

## Skipped/Not Run

- 분석 계획이므로 full eval 재실행은 기본 검증에서 제외한다.

## Validation Result

- Pre-flight checks: 통과.
  - 최신 유효 리포트 `eval/results/eval_20260514_180006.json` 확인.
  - `eval/pipeline.py`의 faithfulness prompt와 `context_texts[:3]` 사용 확인.
  - `tc-10` retrieved context를 동일 RAG retrieval 경로로 추출.
- Automated tests: 통과.
  - `bash scripts/validate-docs.sh`
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- Manual/Runtime QA: 통과.
  - `tc-10` 답변의 핵심 문장은 context 1, 2에 직접 근거함을 확인.
  - context 3은 이용 제한/해지 조항으로 `tc-10` 답변 근거와 무관함을 확인.
- Single-case judge reproduction: 통과.
  - `context_texts[:2]`: `YES`
  - `context_texts[:3]`: `NO`
  - `context_texts[:5]`: `NO`
- Skipped/Not Run:
  - 계획대로 full eval 재실행은 미실행.

## Open Work

- 이 계획 범위의 남은 작업은 없다.
- 후속 작업은 faithfulness 전용 context selection 구현 실험이다.

## Completion

- `tc-10` faithfulness 실패 원인은 답변 근거 부족보다 judge context selection 문제로 분류했다.
- 분석 결과를 `docs/references/2026-05-15-faithfulness-eval-stability.md`에 기록했다.
- 다음 후보는 `context_texts[:3]` 고정 사용을 대체하는 faithfulness 전용 context selection이다.
