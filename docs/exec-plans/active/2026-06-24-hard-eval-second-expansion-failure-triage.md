# Hard Eval Second Expansion Failure Triage Plan

## Goal

hard eval 2차 확장 후 critical로 잡힌 `tc-07`, `tc-28`, `tc-29`, `tc-34`, `tc-37`의 원인을 focused run으로 분류한다.

## Scope

- 실패 5건의 saved answer와 expected keyword 비교
- focused 반복 실행으로 실패 안정성 확인
- 각 케이스를 `answer generation`, `eval rule`, `question wording`, `retrieval ordering`, `faithfulness judge` 중 하나로 분류
- 필요한 최소 보정 후보 정리

## Out Of Scope

- 즉시 prompt 변경
- 즉시 retrieval/rerank 변경
- 모델 교체
- 운영 API/Web 배포
- concise mode 변경

## Assumptions

- 기준 report는 `eval/results/eval_20260624_151136.json`이다.
- 실패 5건 모두 `source_recall_at_k=1.0`, `rag_normalized_source_precision_at_k=1.0`, `faithfulness=1.0`이다.
- primary 후보는 answer coverage, eval rule, question wording이다.

## Pre-flight Checks

- [ ] `git status --short --branch`
- [ ] `bash scripts/validate-docs.sh`
- [ ] `eval/results/eval_20260624_151136.json`의 실패 5건 확인

## Steps

1. 실패 5건의 full eval answer와 expected keyword를 표로 정리한다.
2. 서버에서 실패 5건 focused set을 3회 반복 실행한다.
3. 반복 실패가 있는 케이스와 일회성 실패를 분리한다.
4. `tc-07`, `tc-29`, `tc-37`은 deterministic keyword OR group 문제인지 먼저 확인한다.
5. `tc-28`, `tc-34`는 question wording과 answer coverage 중 어느 쪽인지 확인한다.
6. 보정이 필요하면 별도 implementation step에서 최소 변경만 적용한다.
7. focused smoke 통과 후 full eval 재실행 여부를 결정한다.

## Automated Tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m json.tool eval/test_cases.json > /tmp/test_cases_validated.json`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py`

## Manual/Runtime QA

- focused run 답변이 실제 문서 근거를 벗어나지 않는지 확인한다.
- eval rule 보정 시 실제 답변 동의 표현만 좁게 허용한다.
- question wording 보정 시 expected keyword 범위와 질문 범위를 일치시킨다.

## Skipped/Not Run

- 아직 focused 반복 실행 전이다.
- 아직 보정 변경은 적용하지 않았다.

## Observation Log

- 기존 active plan에 agent loop 하네스 검증 계약을 맞추기 위해 이 섹션을 추가했다.
- 아직 focused 반복 실행 전이며, 실패 원인 분류 작업은 open work로 유지한다.

## Open Work

- focused 반복 실행
- 실패 원인 분류
- 최소 보정 후보 작성

## Validation Result

- Not run for completion.
- 이 plan은 focused 반복 실행과 실패 원인 분류 전까지 active 상태로 유지한다.
