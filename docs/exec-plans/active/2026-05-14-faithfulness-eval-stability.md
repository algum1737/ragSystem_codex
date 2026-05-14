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

- 아직 실행 전.

## Open Work

- `tc-10` faithfulness 판정 흔들림 원인 분석
