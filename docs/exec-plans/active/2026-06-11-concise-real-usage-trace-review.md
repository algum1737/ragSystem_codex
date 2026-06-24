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

### 2026-06-19 14:56 KST

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
trace_mtime=2026-06-19T11:50:43+09:00
total_records=351
api.query=44
eval.case=307
api.answer_mode.standard=9
api.answer_mode.concise=13
post_2026_06_12_063219Z_concise_count=6
post_2026_06_12_063219Z_smoke_like_count=3
post_2026_06_12_063219Z_non_smoke_candidate_count=3
post_non_smoke_candidate_answer_length_mean=393.00
post_non_smoke_candidate_total_ms_mean=9220.42
post_non_smoke_candidate_llm_ms_mean=9099.82
post_non_smoke_candidate_retrieval_ms_mean=120.41
post_non_smoke_candidate_source_count_values=[5]
```

판단:

- 이전 checkpoint 이후 full eval로 `eval.case` trace가 크게 늘었고, `api.query`도 `38 -> 44`로 증가했다.
- `answer_mode=concise` API 표본은 `7 -> 13`으로 늘었다.
- 2026-06-12T06:32:19Z 이후 `concise` 6건 중 3건은 같은 question hash가 1분 안에 3회 반복된 smoke-like 표본으로 분류한다.
- 나머지 3건은 실제 사용자 후보 표본이지만 trace에는 질문/답변 본문이 없으므로 품질 판단을 확정할 수 없다.
- 후보 3건은 모두 source 5개를 유지했고 answer length는 383~405자로 concise 길이 기준 안에 있다.
- 후보 3건 평균 total latency는 9220.42ms이고, 병목은 LLM 구간이다.
- 실제 사용자 후보 표본이 3건뿐이므로 prompt 변경, eval case 추가, full eval은 실행하지 않는다.
- 이 plan은 완료하지 않고 active 상태로 유지한다.

### 2026-06-15 KST

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
trace_mtime=2026-06-12T06:32:19Z
total_records=61
api.query=38
api.answer_mode.standard=9
api.answer_mode.concise=7
post_fix_concise_count=1
post_fix_smoke_like_count=1
post_fix_non_smoke_count=0
```

판단:

- 이전 checkpoint 이후 API trace는 `api.query=32 -> 38`로 늘었다.
- 증가분은 `standard` 표본 중심이며 `concise` 표본은 `7`건으로 변동이 없다.
- post-fix 이후 실제 사용자 `concise` 표본은 아직 없다.
- 이 plan은 완료하지 않고 active 상태로 유지한다.
- 추가 prompt 변경, eval case 추가, full eval은 실행하지 않는다.

### 2026-06-18 KST

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
trace_mtime=2026-06-12T06:32:19Z
total_records=61
api.query=38
api.answer_mode.standard=9
api.answer_mode.concise=7
post_fix_concise_count=1
post_fix_smoke_like_count=1
post_fix_non_smoke_count=0
post_fix_answer_length_mean=376.0
post_fix_total_ms_mean=14664.74
post_fix_source_count_values=[5]
```

판단:

- 이전 checkpoint 이후 trace 파일 mtime과 집계가 변하지 않았다.
- post-fix 이후 실제 사용자 `concise` 표본은 아직 없다.
- 유일한 post-fix `concise` 표본은 이전 `concise-06` smoke question hash다.
- 이 plan은 완료하지 않고 active 상태로 유지한다.
- 추가 prompt 변경, eval case 추가, full eval은 실행하지 않는다.

### 2026-06-24 11:19 KST

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
trace_mtime=2026-06-19T15:01:05+09:00
total_records=352
api.query=45
eval.case=307
api.answer_mode.standard=10
api.answer_mode.concise=13
after_2026_06_19_checkpoint_api_query=1
after_2026_06_19_checkpoint_standard_count=1
after_2026_06_19_checkpoint_concise_count=0
post_2026_06_12_063219Z_concise_count=6
post_2026_06_12_063219Z_smoke_like_count=3
post_2026_06_12_063219Z_non_smoke_candidate_count=3
post_non_smoke_candidate_answer_length_mean=393.00
post_non_smoke_candidate_total_ms_mean=9220.42
post_non_smoke_candidate_llm_ms_mean=9099.82
post_non_smoke_candidate_retrieval_ms_mean=120.41
post_non_smoke_candidate_source_count_values=[5]
```

판단:

- 이전 checkpoint 이후 trace는 1건 증가했고, 증가분은 `answer_mode=standard` API query다.
- `answer_mode=concise` API 표본은 `13`건으로 변동이 없다.
- 2026-06-12T06:32:19Z 이후 실제 사용자 후보 `concise` 표본도 3건으로 변동이 없다.
- 신규 concise 표본이 없으므로 prompt 변경, eval case 추가, full eval은 실행하지 않는다.
- 이 plan은 완료하지 않고 active 상태로 유지한다.

### 2026-06-24 11:28 KST

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
trace_mtime=2026-06-19T15:01:05+09:00
total_records=352
api.query=45
eval.case=307
api.answer_mode.standard=10
api.answer_mode.concise=13
after_5th_checkpoint_records=0
after_5th_checkpoint_api_query=0
after_5th_checkpoint_concise_count=0
post_2026_06_12_063219Z_concise_count=6
post_2026_06_12_063219Z_smoke_like_count=3
post_2026_06_12_063219Z_non_smoke_candidate_count=3
post_non_smoke_candidate_answer_length_mean=393.00
post_non_smoke_candidate_total_ms_mean=9220.42
post_non_smoke_candidate_llm_ms_mean=9099.82
post_non_smoke_candidate_retrieval_ms_mean=120.41
post_non_smoke_candidate_source_count_values=[5]
```

판단:

- 5차 checkpoint 이후 trace 파일 mtime과 행 수가 변하지 않았다.
- 신규 API query와 신규 `answer_mode=concise` 표본은 없다.
- 2026-06-12T06:32:19Z 이후 실제 사용자 후보 `concise` 표본은 계속 3건이다.
- 신규 concise 표본이 없으므로 prompt 변경, eval case 추가, full eval은 실행하지 않는다.
- 이 plan은 완료하지 않고 active 상태로 유지한다.
