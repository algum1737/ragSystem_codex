# Concise Real Usage Trace Review Plan

## Goal

`concise` answer mode의 실제 사용자 표본이 더 쌓인 뒤 운영 trace를 다시 검토해 post-fix prompt가 불필요한 bullet을 줄이고 필수 예외를 유지하는지 확인한다.

## Scope

- 최근 `api.query` trace 중 `answer_mode=concise` 표본 집계
- post-fix 이후 실제 사용자 표본과 smoke 표본 분리
- answer length, latency, source count 추세 확인
- 필요 시 추가 경량 eval case 후보 정리

## Out Of Scope

- 즉시 prompt 변경
- full eval 실행
- 운영 기본 answer mode 변경
- trace payload에 full answer 저장

## Assumptions

- trace는 privacy-safe metadata 중심으로 유지한다.
- 실제 사용자 표본이 충분하지 않으면 작업을 완료하지 않고 open work로 남긴다.
- full answer는 trace에 저장하지 않으므로 품질 판단은 필요 시 별도 승인된 smoke로 보완한다.

## Pre-flight checks

- `git status --short --branch`
- 서버 `/health`
- 최근 trace 파일 존재 여부

## Steps

1. 최근 `rag_traces.jsonl`에서 `answer_mode=concise` API 표본을 집계한다.
2. post-fix 이후 timestamp 기준으로 실제 사용자 표본과 작업 smoke 표본을 분리한다.
3. latency, answer length, source count를 이전 post-fix smoke와 비교한다.
4. 품질 판단이 필요한 질문이 있으면 별도 smoke 실행 필요 여부를 결정한다.
5. 추가 경량 eval case 확장 여부를 정리한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 health 확인
- 운영 trace 표본 확인

## Skipped/Not Run

- full eval은 실행하지 않는다. 운영 trace review 범위다.

## Open Work

- 실제 사용자 concise trace 표본 확보 후 재검토

## Checkpoints

### 2026-06-11 13:00 KST

서버 health는 정상이다.

```text
ragsystem-api: active
ragsystem-web: active
API /health: {"status":"ok","model":"gemma3:12b"}
Streamlit _stcore/health: ok
```

운영 trace 집계:

```text
trace_file=/opt/ragSystem_codex/logs/rag_traces.jsonl
trace_mtime=2026-06-11T04:11:08Z
total_records=55
api.query=32
api.answer_mode.concise=7
post_fix_concise_count=1
post_fix_smoke_like_count=1
post_fix_non_smoke_count=0
```

판단:

- post-fix 이후 실제 사용자 `concise` 표본은 아직 없다.
- 유일한 post-fix `concise` 표본은 이전 `concise-06` smoke question hash다.
- 이 plan은 완료하지 않고 active 상태로 유지한다.
- 추가 prompt 변경, eval case 추가, full eval은 실행하지 않는다.
