# Hard Eval Second Expansion Plan

## Goal

32개 hard eval green baseline 이후에도 남아 있을 수 있는 답변 품질 gap을 찾기 위해 hard eval을 2차 확장한다.

## Scope

- 기존 `eval/test_cases.json` 32개 케이스의 coverage gap 확인
- 약관 도메인별 hard case 후보 6~8개 추가
- 추가 케이스는 retrieval/source recall과 answer coverage를 함께 흔드는 질문으로 작성
- 로컬 retrieval-only smoke 실행
- 서버 `gemma3:12b + top_k=5` full eval 실행
- 실패가 나오면 `retrieval`, `answer generation`, `eval rule`, `question wording`, `faithfulness judge` 중 하나로 분류
- 결과 문서와 source drift report 작성

## Out Of Scope

- prompt 변경
- retrieval/rerank 변경
- 모델 교체
- fine-tuning
- 운영 API/Web 배포
- concise mode 변경

## Assumptions

- 현재 기준선은 `eval/results/eval_20260619_115043.json`이다.
- 기준선 지표는 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0`, `source_recall@k_mean=1.0`, `rag_normalized_source_precision@k_mean=1.0`이다.
- 신규 케이스는 모델을 바로 개선하기보다 실패 후보를 찾는 eval-first 작업이다.
- 질문/expected keyword가 실제 문서 근거보다 넓어지면 `tc-30`, `tc-31`처럼 false failure가 생길 수 있으므로 케이스별 evidence range를 좁게 잡는다.

## Candidate Coverage

우선순위 후보:

1. 위치정보 제3자 제공/통보와 즉시 통보 예외
2. 위치정보 보호의무자 권리와 8세 이하 아동 등 대상 범위
3. 계정/운영정책의 제재 단계와 이의제기 또는 해제 절차
4. 게시물 운영정책의 임시조치/재게시/권리침해 처리
5. 유료서비스 청약철회 제한과 환불 산정의 다중 조건
6. 서비스 변경/중단/종료 고지의 문서별 차이
7. no-answer hard case 1건: 문서에 직접 근거 없는 금액/기간/비율 질문

## Pre-flight Checks

- [x] `git status --short --branch`
- [x] `bash scripts/validate-docs.sh`
- [ ] 기존 32개 케이스 중 신규 후보와 중복되는 질문 확인

## Steps

1. 실제 인제스천 source filename과 기존 32개 케이스 coverage를 확인한다.
2. `eval/test_cases.json`에 `tc-33`부터 신규 hard case를 추가한다.
3. JSON schema와 Python compile을 확인한다.
4. 로컬 retrieval-only smoke를 실행한다.
5. 서버에 `eval/test_cases.json`을 반영한다.
6. 서버 full eval을 실행한다.
7. full eval report를 로컬 `eval/results/`에 복사한다.
8. source drift report를 생성한다.
9. 실패 케이스를 원인별로 분류한다.
10. 결과 문서, `docs/index.md`, `docs/HANDOFF.md`, 이 plan을 갱신한다.

## Automated Tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m json.tool eval/test_cases.json > /tmp/test_cases_validated.json`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py`
- `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`
- `.venv/bin/python eval/pipeline.py --metric retrieval --model gemma3:12b --top-k 5`

## Server Eval

```bash
cd /opt/ragSystem_codex
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
CUDA_VISIBLE_DEVICES="" \
.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
```

## Expected Results

- Retrieval smoke는 신규 케이스 포함 `source_recall@k_mean >= 0.95`, `rag_normalized_source_precision@k_mean >= 0.95`를 유지한다.
- Full eval은 실패가 발생해도 실패 원인을 분류할 수 있어야 한다.
- 실패가 없으면 2차 확장 baseline을 새 green baseline으로 기록한다.
- 실패가 있으면 즉시 prompt/retrieval 변경으로 가지 않고 focused triage plan을 별도로 세운다.

## Manual/Runtime QA

- 신규 케이스 질문이 expected keyword와 같은 evidence range를 요구하는지 확인한다.
- 다중 문서 질문은 질문에 비교 대상 문서를 명시한다.
- no-answer 케이스는 문서에 직접 근거가 없는 질문인지 확인한다.

## Skipped/Not Run

- Prompt 변경은 실행하지 않았다.
- Retrieval/rerank 변경은 실행하지 않았다.
- 운영 API/Web 배포는 실행하지 않았다.

## Open Work

- 실패 5건 focused triage는 별도 active plan에서 진행한다.

## Completion

- 완료.
- `eval/test_cases.json`에 `tc-33`~`tc-39` 7개 hard case를 추가했다.
- 로컬 retrieval-only smoke는 `source_recall@k_mean=1.0`, `rag_normalized_source_precision@k_mean=1.0`이다.
- 서버 full eval report는 `eval/results/eval_20260624_151136.json`이다.
- full eval 지표는 `accuracy_mean=0.9711`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0`, `source_recall@k_mean=1.0`, `rag_normalized_source_precision@k_mean=1.0`이다.
- critical case는 `tc-07`, `tc-28`, `tc-29`, `tc-34`, `tc-37`이다.
- 결과 문서: `docs/references/2026-06-24-hard-eval-second-expansion-result.md`
- Source drift report: `docs/references/2026-06-24-hard-eval-second-expansion-source-drift-report.md`
- 후속 active plan: `docs/exec-plans/active/2026-06-24-hard-eval-second-expansion-failure-triage.md`

## Validation Result

- 통과: `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: `.venv/bin/python -m json.tool eval/test_cases.json > /tmp/test_cases_validated.json`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py`
- 통과: `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`
- 통과: `.venv/bin/python eval/pipeline.py --metric retrieval --model gemma3:12b --top-k 5`
  - `total_cases=39`
  - `source_recall@k_mean=1.0`
  - `rag_normalized_source_precision@k_mean=1.0`
  - `rag_chunk_precision@k_mean=0.8256`
- 부분 통과: 서버 full eval
  - report: `eval/results/eval_20260624_151136.json`
  - `accuracy_mean=0.9711`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - `rag_normalized_source_precision@k_mean=1.0`
  - critical cases: `tc-07`, `tc-28`, `tc-29`, `tc-34`, `tc-37`
