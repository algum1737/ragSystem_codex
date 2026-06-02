# Trace Runtime Verification Plan

## Goal

Ubuntu 서버에서 local trace sink가 systemd API 서비스와 eval 실행에서 의도대로 동작하는지 검증한다.

## Scope

- `RAG_TRACE_ENABLED`/`RAG_TRACE_PATH` systemd 적용 절차 확인
- API query 1건 실행 후 JSONL event 생성 확인
- eval smoke 실행 후 `eval.case` event 생성 확인
- trace payload에 full prompt, full answer, chunk text가 없는지 재확인

## Out Of Scope

- Langfuse Cloud 연동
- self-hosted Langfuse 배포
- trace dashboard 구현
- 성능 튜닝 파라미터 변경

## Assumptions

- Ubuntu 서버 주소는 기존 운영 확인 대상인 `10.10.220.5`이고 계정은 `ragadmin`이다.
- 서버 파일 배포와 systemd 수정은 사용자가 서버에서 직접 실행하거나 별도 승인 후 진행한다.
- trace는 기본 off 상태를 유지하고, 검증 시에만 명시적으로 켠다.

## Pre-flight checks

- 로컬 변경 사항 commit/push 상태 확인
- 서버 배포본이 최신 commit을 포함하는지 확인
- `ragsystem-api.service` 현재 상태 확인
- trace output directory 권한 확인

## Steps

1. 서버에 최신 변경을 배포한다.
2. systemd override 또는 service file에 trace 환경변수를 적용한다.
3. API 서비스를 재시작하고 `/health`를 확인한다.
4. query 1건을 실행하고 JSONL event를 확인한다.
5. eval smoke를 실행하고 `eval.case` event를 확인한다.
6. trace payload에 민감 본문이 없는지 샘플을 점검한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile api/main.py retriever/engine.py eval/pipeline.py query.py observability/trace.py`

## Manual/Runtime QA

- `journalctl -u ragsystem-api.service -f`에서 query 중 서버 crash 없음 확인
- `tail -n 5 /opt/ragSystem_codex/logs/rag_traces.jsonl` 샘플 확인
- Streamlit query tab에서 API 연결과 답변 반환 확인

## Skipped/Not Run

- 아직 서버 적용 전이다.

## Open Work

- Ubuntu 서버에 최신 변경 배포.
- systemd trace 환경변수 적용과 실제 runtime trace 확인.
