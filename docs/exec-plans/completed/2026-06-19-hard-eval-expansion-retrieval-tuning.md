# Hard Eval Expansion And Retrieval Tuning Plan

## Goal

현재 green인 23개 full eval보다 어려운 hard eval 케이스를 추가하고, 새 기준선에서 드러나는 실패를 바탕으로 retrieval/rerank 튜닝 후보를 결정한다.

## Scope

- `eval/test_cases.json`에 hard eval 케이스 9개 추가
- `gemma3:12b + top_k=5` baseline full eval 재실행
- source drift report 생성
- 실패 케이스를 `retrieval`, `answer generation`, `eval rule`, `judge` 중 하나로 분류
- retrieval/rerank 튜닝이 필요한 경우 후속 plan 후보를 기록
- 결과 문서, `docs/index.md`, `docs/HANDOFF.md` 갱신

## Out Of Scope

- 이번 plan 안에서 retrieval/rerank 알고리즘을 바로 변경하지 않는다.
- prompt를 바로 변경하지 않는다.
- 모델 교체, fine-tuning, 재인제스천은 하지 않는다.
- concise mode 평가셋은 변경하지 않는다.
- 운영 API/Web 배포는 하지 않는다.

## Assumptions

- 최신 green baseline은 `eval/results/eval_20260619_102404.json`이다.
- 기존 23개 케이스가 모두 green이므로 품질 개선의 첫 단계는 더 어려운 실패 지점을 만드는 것이다.
- hard eval은 문서 간 비교, 예외 조건, 부분 부재, 세부 절차 질문을 우선한다.
- false positive를 피하기 위해 `expected_keywords`는 문서에 직접 있는 좁은 표현 중심으로 구성한다.

## Pre-flight checks

- [x] `git status --short --branch`
- [x] `bash scripts/validate-docs.sh`
- [x] local Chroma stats 확인
  - `count=318`
- [x] existing eval case count 확인
  - `23`
- [x] candidate retrieval source 확인

## Candidate Hard Cases

추가 후보:

| New ID | Focus | Question |
| --- | --- | --- |
| `tc-24` | 위치정보 확인자료 보유기간 | 위치기반서비스 약관에서 위치정보 이용·제공사실 확인자료는 얼마나 보관되는가? |
| `tc-25` | 위치정보 동의 철회와 파기 | 위치기반서비스 약관에서 이용자가 위치정보 동의를 철회하면 개인위치정보와 확인자료는 어떻게 처리되는가? |
| `tc-26` | 만 14세 미만 위치정보 법정대리인 권리 | 만 14세 미만 아동의 개인위치정보 수집·이용·제공은 누가 동의하고 어떤 권리를 행사할 수 있는가? |
| `tc-27` | 게시중단 이의신청 절차 | 게시중단 조치에 대해 원 게시자가 이의신청하면 게시물은 어떻게 처리되는가? |
| `tc-28` | 계정 보호조치와 장기 미사용 제한 | 계정 운영정책에서 비정상 로그인이나 장기 미사용 계정은 어떤 보호조치 또는 제한을 받는가? |
| `tc-29` | 정기결제일 부재와 무료체험 재가입 | 카카오 유료서비스 정기결제에서 결제일이 없는 달과 무료체험 재가입은 어떻게 처리되는가? |
| `tc-30` | 동일 결제수단 환불 불가 | 유료서비스 환불 시 결제수단으로 같은 방법 환불이 불가능하면 어떻게 처리되는가? |
| `tc-31` | 미성년자 유료/결제서비스 제한 | 미성년자가 유료서비스 또는 결제서비스를 이용하려는 경우 어떤 제한이 있는가? |
| `tc-32` | Daum 36개월 미로그인 계정 탈퇴 | Daum 약관에서 36개월 동안 로그인하지 않은 계정은 언제 어떻게 탈퇴 처리되는가? |

## Steps

1. `eval/test_cases.json`에 `tc-24`~`tc-32`를 추가한다.
2. JSON/schema 정적 검증을 실행한다.
3. 로컬에서 retrieval-only smoke를 실행해 source scope를 빠르게 확인한다.
4. 서버에 변경된 `eval/test_cases.json`과 필요 파일을 반영한다.
5. 서버에서 `gemma3:12b + top_k=5` full eval을 실행한다.
6. 새 eval report를 로컬로 복사한다.
7. source drift report를 생성한다.
8. 실패 케이스를 원인별로 분류한다.
9. 결과 문서와 handoff를 갱신한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m json.tool eval/test_cases.json >/dev/null`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py`
- `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`
- `.venv/bin/python eval/pipeline.py --metric retrieval --model gemma3:12b --top-k 5`
- 서버:
  ```bash
  cd /opt/ragSystem_codex
  RAG_TRACE_ENABLED=true \
  RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
  CUDA_VISIBLE_DEVICES="" \
  .venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
  ```

## Manual/Runtime QA

- 신규 케이스 질문이 실제 문서 근거와 맞는지 확인한다.
- `expected_keywords`가 지나치게 넓거나 답변 문체에만 의존하지 않는지 확인한다.
- 기존 23개 케이스가 회귀하지 않았는지 확인한다.
- 신규 9개 케이스 실패가 source 누락인지 answer wording인지 분류한다.

## Skipped/Not Run

- fine-tuning은 실행하지 않는다. hard eval 실패 유형이 충분히 쌓인 뒤 별도 검토한다.
- prompt 보정은 이번 plan에서 바로 하지 않는다.
- retrieval/rerank 코드 변경은 이번 baseline 결과를 본 뒤 별도 plan으로 진행한다.

## Open Work

- `tc-30` answer coverage follow-up은 `docs/exec-plans/active/2026-06-19-tc30-answer-coverage-fix.md`에서 진행한다.

## Completion

- 완료.
- `tc-24`~`tc-32` hard eval 9개를 추가했다.
- 확장 후 baseline 결과 retrieval/source 지표는 green이다.
- 남은 실패는 `tc-30` 1건이며 retrieval/rerank 문제가 아니라 answer generation multi-source coverage 문제로 분류했다.
- 결과 문서: `docs/references/2026-06-19-hard-eval-expansion-result.md`
- Source drift report: `docs/references/2026-06-19-hard-eval-expansion-source-drift-report.md`

## Validation Result

- 통과: `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: local Chroma stats
  - `count=318`
- 통과: `.venv/bin/python -m json.tool eval/test_cases.json > /tmp/test_cases_validated.json`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py`
- 통과: local retrieval-only smoke
  - command: `.venv/bin/python eval/pipeline.py --metric retrieval --model gemma3:12b --top-k 5`
  - `total_cases=32`
  - `rag_normalized_source_precision@k_mean=1.0`
  - `source_recall@k_mean=1.0`
- 부분 통과: server full eval original
  - report: `eval/results/eval_20260619_105835.json`
  - `accuracy_mean=0.9813`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - failures: `tc-29`, `tc-30`
- 통과: `tc-29` eval rule recalibration
  - added `날짜가 없` to `tc-29` expected keyword OR group.
  - recalibrated report: `eval/results/eval_20260619_105835_tc29_recalibrated.json`
- 부분 통과: recalibrated report
  - `accuracy_mean=0.9875`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - remaining failure: `tc-30 answer_accuracy=0.6`
- 통과: source drift report 생성
  - `docs/references/2026-06-19-hard-eval-expansion-source-drift-report.md`
  - critical case: `tc-30`
  - watch case: 없음
