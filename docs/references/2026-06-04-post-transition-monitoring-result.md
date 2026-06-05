# 2026-06-04 Post Transition Monitoring Result

## Summary

`gemma3:12b + top_k=5` 운영 전환은 정상 동작한다.

전환 후 대표 API query들은 `gemma4:26b` 시절의 200초대 지연보다 크게 개선됐다. 다만 LLM 생성 구간은 여전히 주 병목이므로, 다음 튜닝 후보는 `gemma3:12b` 전용 `max_tokens` 제한 실험이다.

## Server State

확인 결과:

- `/health`: `{"status":"ok","model":"gemma3:12b"}`
- `/stats`: `{"collection_name":"ragSystem","count":318}`
- Streamlit: `HTTP/1.1 200 OK`
- 추가 query 후 `ollama ps`: `gemma3:12b`, `100% GPU`, context 4096

추가 query 전 idle 상태에서는 `ollama ps`가 비어 있었고 GPU 메모리는 거의 비어 있었다.

## Additional Query Samples

대표 query 2건을 추가 실행했다.

| Query | Doc type | Elapsed | Answer length | Sources |
| --- | --- | ---: | ---: | ---: |
| 위치기반서비스 약관에서 개인위치정보는 어떤 목적으로 이용되는가? | 위치기반서비스 | 24.78s | 426 | 5 |
| 운영정책에서 계정 이용이 제한되거나 해지될 수 있는 조건은 무엇인가? | 운영정책 | 7.72s | 617 | 5 |

## Trace Review

전환 후 주요 `api.query` trace:

| Timestamp | Doc type | Total | Retrieval | LLM | Answer length |
| --- | --- | ---: | ---: | ---: | ---: |
| 2026-06-04T08:44:19Z | 전체 | 22.05s | 0.14s | 21.91s | 998 |
| 2026-06-04T09:08:23Z | 위치기반서비스 | 24.77s | 9.57s | 15.20s | 426 |
| 2026-06-04T09:08:31Z | 운영정책 | 7.71s | 0.12s | 7.60s | 617 |

The location-service query included a cold embedding/rerank load:

- embedding: about 8.19s
- rerank: about 1.32s

Warm retrieval is otherwise around 0.12-0.14s in the observed samples.

## Decision

No immediate model, `top_k`, prompt, or GPU configuration change is needed.

Next tuning candidate:

1. `gemma3:12b` token cap experiment
   - Reason: LLM generation remains the dominant latency contributor.
   - Prior evidence: `gemma3:12b` handled `max_tokens`/`num_predict` normally in earlier latency triage.
2. API embedding/reranker CPU mode is deferred.
   - Reason: current idle GPU memory is low and Ollama runs `gemma3:12b` as `100% GPU`.
3. `top_k=4` is deferred.
   - Reason: `top_k=5` preserves source recall; `top_k=3` already showed quality regression.

## Next Work

Open a focused `gemma3:12b` token cap experiment plan.
