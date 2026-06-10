# Concise Eval Server Verification Plan

## Goal

로컬에서 구현한 concise lightweight eval harness를 Ubuntu 서버에 반영하고 운영 GPU/Ollama 환경에서 smoke 결과를 확인한다.

## Scope

- 서버에 `eval/pipeline.py`, `eval/concise_test_cases.json` 반영
- 서버 py_compile 확인
- 서버 `--concise-lightweight` smoke 실행
- 서버 trace와 결과 JSON 확인

## Out Of Scope

- 운영 API/Web 기능 변경
- 운영 기본 answer mode 변경
- 자동 라우팅 구현
- standard full eval 재실행

## Assumptions

- 서버는 기존 운영 대상 `10.10.220.5`다.
- 서버 계정과 경로는 기존 handoff 기준 `ragadmin`, `/opt/ragSystem_codex`다.
- 서버 반영은 사용자 승인 후 진행한다.

## Pre-flight checks

- `git status --short --branch`
- 서버 `/health`
- 서버 작업트리 또는 배포 경로 상태 확인

## Steps

1. 변경 파일을 서버에 반영한다.
2. 서버에서 py_compile을 실행한다.
3. `RAG_TRACE_ENABLED=true`와 별도 trace path로 concise lightweight eval smoke를 실행한다.
4. 결과 JSON과 trace route `eval.concise`/`eval.concise.case`를 확인한다.
5. 결과를 문서와 handoff에 기록한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- 서버 `.venv/bin/python -m py_compile eval/pipeline.py`
- 서버 concise lightweight eval smoke

## Manual/Runtime QA

- 서버 API `/health`
- 서버 trace tail 확인

## Skipped/Not Run

- full eval은 실행하지 않는다.

## Open Work

- 없음

## Completion

- 서버 API `/health`에서 `status=ok`, `model=gemma3:12b`를 확인했다.
- 서버 `/opt/ragSystem_codex`에 `eval/pipeline.py`와 `eval/concise_test_cases.json`을 반영했다.
- 서버 Python으로 `eval/concise_test_cases.json` JSON load와 6개 케이스 확인을 완료했다.
- 서버 `.venv/bin/python -m py_compile eval/pipeline.py`가 통과했다.
- 서버 `--concise-lightweight` smoke가 6개 케이스 모두 통과했다.
- trace path `/opt/ragSystem_codex/logs/concise_lightweight_eval_20260610.jsonl`에서 `eval.concise`와 `eval.concise.case` route를 확인했다.
- smoke 이후 API `/health`는 정상이다.
- 결과 문서는 `docs/references/2026-06-10-concise-eval-server-verification-result.md`에 기록했다.
- 다음 active plan은 `docs/exec-plans/active/2026-06-10-concise-eval-ci-promotion.md`다.

## Validation Result

- Pre-flight checks: 통과
  - `git status --short --branch`: `## main...origin/main`
  - 서버 `/health`: `{"status":"ok","model":"gemma3:12b"}`
  - 서버 기존 상태: `eval/concise_test_cases.json` 없음, `eval/pipeline.py` 이전 버전 확인
- Automated tests: 통과
  - 서버 Python JSON load: `json_ok`, `concise_cases 6`
  - 서버 `.venv/bin/python -m py_compile eval/pipeline.py`
  - 서버 concise lightweight eval smoke: `total_cases=6`, `passed_cases=6`, `pass_rate=1.0`
- Manual/Runtime QA: 통과
  - trace tail에서 `eval.concise`, `eval.concise.case`, `metadata.answer_mode=concise` 확인
  - smoke 이후 서버 `/health`: `{"status":"ok","model":"gemma3:12b"}`
- Skipped/Not Run: full eval은 실행하지 않았다. 이번 작업은 concise 전용 server smoke 검증 범위다.
