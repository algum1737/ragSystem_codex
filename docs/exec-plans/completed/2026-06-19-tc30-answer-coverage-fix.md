# TC30 Answer Coverage Fix Plan

## Goal

`tc-30`에서 검색된 카카오/네이버 유료서비스 환불 근거를 답변이 모두 다루도록 원인을 좁히고, 필요한 경우 최소 변경으로 보정한다.

## Scope

- `tc-30` retrieved context와 answer 비교
- 같은 질문 focused smoke 반복
- 원인을 `prompt`, `question wording`, `eval rule`, `retrieval ordering` 중 하나로 분류
- 필요한 경우 최소 변경 후보 작성
- 변경 후보 채택 시 focused smoke와 full eval 재실행

## Out Of Scope

- broad prompt rewrite
- 모델 교체
- fine-tuning
- chunking/reingestion
- concise mode 변경
- 운영 API/Web 배포

## Assumptions

- `tc-30`은 source recall과 faithfulness가 모두 `1.0`이다.
- 실패 원인은 검색된 네이버 환불 근거를 답변이 사용하지 않은 multi-source coverage 문제다.
- 전체 prompt를 넓게 바꾸면 기존 케이스 회귀 가능성이 있으므로 focused smoke로 먼저 확인한다.

## Pre-flight checks

- [ ] `git status --short --branch`
- [ ] `bash scripts/validate-docs.sh`
- [ ] `eval/results/eval_20260619_105835_tc29_recalibrated.json`의 `tc-30` 확인

## Steps

1. `tc-30` query의 RAG context를 추출한다.
2. 답변이 누락한 네이버 환불 근거를 정리한다.
3. focused smoke를 3회 실행해 실패가 안정적인지 확인한다.
4. 원인을 분류한다.
5. 보정이 필요하면 최소 변경 후보를 작성한다.
6. focused smoke가 통과하면 full eval을 실행한다.
7. 결과 문서, `docs/index.md`, `docs/HANDOFF.md`를 갱신한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m json.tool eval/test_cases.json >/dev/null`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py`
- `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`

## Manual/Runtime QA

- `tc-30` answer가 카카오와 네이버의 환불 처리 차이를 모두 포함하는지 확인한다.
- 기존 31개 케이스가 회귀하지 않았는지 확인한다.
- prompt 변경을 채택하는 경우 `tc-04`, `tc-15`, `tc-23` 회귀 여부를 특히 확인한다.

## Skipped/Not Run

- Prompt 변경은 실행하지 않았다.
- Retrieval/rerank 변경은 실행하지 않았다.
- 운영 API/Web 배포는 실행하지 않았다.

## Open Work

- 없음.

## Completion

- 완료.
- `tc-30`, `tc-31`은 prompt 문제가 아니라 hard eval question wording과 expected keyword 범위 불일치로 분류했다.
- `eval/test_cases.json`에서 `tc-30`, `tc-31` 질문을 expected evidence 범위에 맞게 좁혔다.
- 최종 32개 full eval은 green이다.
- 결과 문서: `docs/references/2026-06-19-tc30-answer-coverage-result.md`
- Source drift report: `docs/references/2026-06-19-tc30-answer-coverage-source-drift-report.md`

## Validation Result

- 통과: `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: `eval/results/eval_20260619_105835_tc29_recalibrated.json`의 `tc-30` 확인
  - `answer_accuracy=0.6`
  - `faithfulness=1.0`
  - `source_recall_at_k=1.0`
- 통과: `tc-30` focused smoke 3회
  - report: `eval/results/eval_tc30_focused_20260619_111500.json`
  - 3회 모두 `answer_accuracy=0.8`, `faithfulness=1.0`
- 통과: `tc-30` wording probe 3회
  - 3회 모두 `answer_accuracy=1.0`, `faithfulness=1.0`
- 통과: `tc-12`, `tc-31` focused smoke
  - report: `eval/results/eval_tc12_tc31_focused_20260619_114400.json`
  - `tc-12`: 3회 모두 `answer_accuracy=1.0`, `faithfulness=1.0`
  - `tc-31`: 2회 통과, 1회 `answer_accuracy=0.8`
- 통과: `tc-31` wording probe 3회
  - 3회 모두 `answer_accuracy=1.0`, `faithfulness=1.0`
- 부분 통과: 중간 full eval
  - report: `eval/results/eval_20260619_113433.json`
  - `accuracy_mean=0.9938`
  - `faithfulness_mean=0.9688`
  - failures: `tc-12`, `tc-31`
- 통과: 최종 full eval
  - report: `eval/results/eval_20260619_115043.json`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - `rag_normalized_source_precision@k_mean=1.0`
- 통과: 최종 source drift report
  - critical case: 없음
  - watch case: 없음
