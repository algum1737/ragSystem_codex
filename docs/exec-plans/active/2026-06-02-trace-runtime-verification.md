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

- systemd service 환경변수 적용과 `ragsystem-api.service` 재시작은 `sudo` 비밀번호가 필요해 미실행.
- Streamlit query tab 수동 확인은 systemd trace 적용 이후 진행 예정.

## Open Work

- 사용자가 서버에서 `sudo systemctl edit ragsystem-api.service`로 trace 환경변수를 적용해야 한다.
- systemd API 서비스 재시작 후 `/opt/ragSystem_codex/logs/rag_traces.jsonl`에 운영 query trace가 생성되는지 확인해야 한다.
- Streamlit query tab에서 API 연결과 답변 반환을 확인해야 한다.

## Progress

- 서버 SSH 접근 확인: `ragadmin@10.10.220.5`
- 운영 API 상태 확인: `ragsystem-api.service` active
- 운영 API health 확인: `{"status":"ok","model":"gemma4:26b"}`
- 최신 코드 배포 완료: `/opt/ragSystem_codex/observability/trace.py` 확인
- 서버 venv compile 확인 완료
- 임시 API `127.0.0.1:8010` trace enabled smoke 완료
- eval retrieval trace smoke 완료
- 상세 결과 기록: `docs/references/2026-06-02-trace-runtime-verification-result.md`

## Validation Result

- 통과: 서버 venv compile
  - `.venv/bin/python -m py_compile api/main.py retriever/engine.py eval/pipeline.py query.py observability/trace.py`
- 통과: 임시 API query trace smoke
  - route `api.query`
  - full answer, question preview, chunk text 기본 미포함
- 통과: eval retrieval trace smoke
  - eval status `0`
  - trace count `23`
  - last route `eval.case`
  - `eval_case_id`, `eval_scores` 기록 확인
- 부분 통과: runtime latency 확인
  - 검색/임베딩/rerank 정상
  - `gemma4:26b` LLM 구간 약 351초로 매우 느림
- 미실행: systemd trace 환경변수 적용
  - 이유: `sudo` 비밀번호 필요
