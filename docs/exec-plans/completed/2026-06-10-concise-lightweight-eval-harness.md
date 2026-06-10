# Concise Lightweight Eval Harness Plan

## Goal

문서로 정의한 concise mode 경량 평가셋을 실행 가능한 eval harness로 반영한다.

## Scope

- `eval/concise_test_cases.json` 추가
- required point, forbidden claim, answer length, source count 기반 deterministic 판정 구현
- `answer_mode=concise` 경로로만 실행되는 smoke/eval 명령 추가
- trace metadata와 결과 JSON에 `answer_mode=concise`를 남기는지 확인

## Out Of Scope

- 운영 기본 answer mode 변경
- 자동 라우팅 구현
- standard full eval 기준 변경
- 프롬프트 변경

## Assumptions

- 사용자 승인 후에만 구현 변경을 진행한다.
- 경량셋 정의는 `docs/references/2026-06-10-concise-lightweight-eval-set.md`를 기준으로 한다.
- 경량셋은 full eval을 대체하지 않는다.

## Pre-flight checks

- `git status --short --branch`
- `docs/references/2026-06-10-concise-lightweight-eval-set.md` 확인
- 구현 승인 여부 확인

## Steps

1. 평가셋 JSON 구조를 추가한다.
2. concise 전용 평가 실행 경로를 구현한다.
3. deterministic 판정 결과와 trace 정보를 결과 JSON에 기록한다.
4. 로컬 또는 서버에서 대표 smoke를 실행한다.
5. 구현 결과와 검증 결과를 문서화한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py query.py app.py`
- concise lightweight eval smoke 명령

## Manual/Runtime QA

- 필요 시 운영 또는 로컬 API에서 `answer_mode=concise` 대표 질의 1건 확인

## Skipped/Not Run

- full eval은 기본적으로 실행하지 않는다. standard 경로 변경이 생기면 별도 실행한다.

## Open Work

- 없음

## Completion

- `eval/concise_test_cases.json`을 추가했다.
- `eval/pipeline.py`에 `--concise-lightweight` 실행 경로를 추가했다.
- concise 경량 평가는 `answer_mode=concise`로만 RAG query를 실행한다.
- required point, forbidden claim, answer length, source count, no-answer 기준을 deterministic check로 판정한다.
- 결과 JSON에는 `answer_mode`, `required_points_score`, `forbidden_claims_hit_count`, `answer_length`, `source_count`, `latency_ms`, `passed`를 기록한다.
- trace에는 `eval.concise`와 `eval.concise.case` route가 남고 metadata에 `answer_mode=concise`가 기록된다.
- 로컬 smoke 결과는 `eval/results/concise_eval_20260610_092710.json`에 저장했다.
- 결과 문서는 `docs/references/2026-06-10-concise-lightweight-eval-harness-result.md`에 기록했다.
- 다음 active plan은 `docs/exec-plans/active/2026-06-10-concise-eval-server-verification.md`다.

## Validation Result

- Pre-flight checks: 통과
  - `git status --short --branch`: `## main...origin/main`
  - `docs/references/2026-06-10-concise-lightweight-eval-set.md` 확인
  - 사용자의 "다음 업무 진행"을 구현 승인으로 보고 진행
- Automated tests: 통과
  - `jq empty eval/concise_test_cases.json`
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py query.py app.py`
  - `bash scripts/validate-docs.sh`
  - `RAG_TRACE_ENABLED=true RAG_TRACE_PATH=/tmp/concise_eval_trace.jsonl .venv/bin/python eval/pipeline.py --concise-lightweight --top-k 5 --model gemma3:12b`
- Manual/Runtime QA: 통과
  - 로컬 Ollama를 임시 기동해 smoke 실행 후 종료
  - concise lightweight eval summary: `total_cases=6`, `passed_cases=6`, `pass_rate=1.0`
  - `/tmp/concise_eval_trace.jsonl`에서 `eval.concise`와 `eval.concise.case` trace 확인
- Skipped/Not Run: standard full eval은 실행하지 않았다. 이번 변경은 concise 전용 eval 경로 추가이며 standard 기본 query 경로는 변경하지 않았다.
