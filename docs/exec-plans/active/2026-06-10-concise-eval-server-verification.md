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

- 사용자 서버 반영 승인
- 서버 concise lightweight eval smoke
