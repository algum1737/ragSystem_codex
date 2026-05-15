# Faithfulness Context Selection Plan

## Goal

faithfulness 평가에서 무관 context가 judge 입력에 섞여 판정이 흔들리는 문제를 줄인다.

## Scope

- `eval/pipeline.py`의 faithfulness context selection 최소 개선
- `tc-10` 단건 judge 안정화 확인
- 최신 기준 full eval 지표와 비교

## Out Of Scope

- 검색 튜닝
- 답변 생성 프롬프트 변경
- 외부 API judge 도입
- 모델 교체

## Assumptions

- 검색 결과 자체는 관련 source를 포함한다.
- 문제는 faithfulness judge에 전달되는 context의 선택 방식이다.
- 질문/답변과 lexical overlap이 높은 context를 우선하면 무관 청크 영향이 줄어든다.

## Pre-flight checks

- `docs/references/2026-05-15-faithfulness-eval-stability.md` 확인
- `eval/pipeline.py`의 faithfulness 함수 확인
- `tc-10` 단건 재현 결과 확인

## Steps

1. faithfulness 전용 context selector를 설계한다.
2. `context_texts[:3]` 고정 사용을 selector 결과로 교체한다.
3. `tc-10` 단건 judge가 `YES`로 바뀌는지 확인한다.
4. full eval로 `accuracy_mean`, `faithfulness_mean`, `not_found_rate`를 확인한다.
5. 결과가 회귀하면 변경을 철회하고 no-op으로 기록한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- `.venv/bin/python eval/pipeline.py --all`

## Manual/Runtime QA

- `tc-10` 답변과 selector가 고른 context를 직접 대조한다.
- 무관한 이용 제한/해지 context가 judge 입력 우선순위에서 밀리는지 확인한다.

## Skipped/Not Run

- UI/API smoke test는 평가 파이프라인 변경만 수행하는 경우 기본 검증에서 제외한다.

## Validation Result

- Pre-flight checks: 통과.
  - `docs/references/2026-05-15-faithfulness-eval-stability.md` 확인.
  - `eval/pipeline.py`의 faithfulness 함수와 기존 `context_texts[:3]` 사용 확인.
  - `tc-10` 단건 재현 결과 확인.
- Automated tests: 통과.
  - `bash scripts/validate-docs.sh`
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
  - `.venv/bin/python eval/pipeline.py --all` 권한 상승 경로에서 통과.
- Manual/Runtime QA: 통과.
  - source diversity selector 적용 후 `tc-03`, `tc-10` 단건 faithfulness가 모두 `1.0`으로 판정됨을 확인.
  - selector가 `tc-03`에서 `네이버 이용약관`, `다음 위치기반서비스 이용약관`, `다음 이용약관` 근거를 모두 포함함을 확인.
  - selector가 `tc-10`에서 `다음 이용약관`, `네이버 이용약관` 근거를 포함함을 확인.
- Full eval result:
  - 리포트: `eval/results/eval_20260515_110900.json`
  - `accuracy_mean=0.95`
  - `faithfulness_mean=1.0`
  - `not_found_rate=0.0`
  - `rag_normalized_source_precision@k_mean=1.0`
  - `source_recall@k_mean=1.0`
- Skipped/Not Run:
  - UI/API smoke test는 계획대로 미실행.

## Open Work

- 이 계획 범위의 남은 작업은 없다.
- 후속 작업은 `tc-03`, `tc-09` 잔여 keyword accuracy 분석이다.

## Completion

- faithfulness judge context selection을 질문/답변 lexical overlap과 source diversity 기준으로 개선했다.
- `tc-10` faithfulness 흔들림은 해결됐고 full eval에서 `faithfulness_mean=1.0`을 회복했다.
- 잔여 병목은 `tc-03`, `tc-09`의 `answer_accuracy=0.75`다.
