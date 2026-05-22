# Eval Failure Triage Plan

## Goal

확장 평가셋 full eval에서 드러난 실패 케이스를 분류하고 우선 개선 대상을 정한다.

## Scope

- `eval/results/eval_20260522_091248.json` 기준 실패 케이스 분석
- negative/no-answer 채점 정책 검토
- 다문서 faithfulness context selection 재검토 후보 선정
- `tc-04`, `tc-06`의 질문/`relevant_sources` 재정의 필요성 검토

## Out Of Scope

- 신규 문서 인제스천
- 모델 교체
- 외부 judge 도입
- 대규모 검색 알고리즘 변경

## Assumptions

- 평가셋은 16개 케이스로 확장됐다.
- 신규 `tc-11`, `tc-12`, `tc-13`은 신규 corpus 검증 케이스로 정상 동작한다.
- `tc-16`은 의도한 negative case이나 현재 평가식에서는 낮은 accuracy/faithfulness로 집계된다.

## Pre-flight checks

- `docs/references/2026-05-22-eval-set-expansion-result.md` 확인
- `eval/results/eval_20260522_091248.json` 확인
- `eval/pipeline.py`의 `not_found`, `answer_accuracy`, `faithfulness` 집계 방식 확인

## Steps

1. `tc-16`에 기대 no-answer를 표현할 수 있는 평가셋 필드 설계를 검토한다.
2. `tc-09`, `tc-10` faithfulness judge 입력 context를 재현하고 실패 원인을 분석한다.
3. `tc-04`, `tc-06`의 source drift가 평가셋 문제인지 검색 문제인지 분리한다.
4. 구현 후보를 작은 변경 단위로 정리한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`

## Manual/Runtime QA

- 실패 케이스 답변과 retrieved source를 직접 대조한다.
- 변경 후보가 기존 10개 케이스를 과도하게 완화하지 않는지 확인한다.

## Skipped/Not Run

- 아직 실행 전.

## Validation Result

- 아직 실행 전.

## Open Work

- 실패 케이스 triage 진행.
