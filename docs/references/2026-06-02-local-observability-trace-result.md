# 2026-06-02 Local Observability Trace Result

## Summary

Langfuse 도입 전 단계로 로컬 JSONL trace sink를 추가했다. trace는 기본 off이며 `RAG_TRACE_ENABLED=true`일 때만 기록된다.

## Implemented

- `observability.trace` 모듈을 추가했다.
- 기본 trace 경로는 `./logs/rag_traces.jsonl`이며 `RAG_TRACE_PATH`로 변경할 수 있다.
- `logs/`를 gitignore에 추가했다.
- API `/query`, CLI query, `RAGEngine.query()` 경계에 route, trace id, model, top_k, retrieved source path, latency, answer length 기록을 연결했다.
- eval pipeline은 `eval.case` event에 `case_id`, model, top_k, retrieved sources, query latency, score 필드를 기록한다.
- trace writer 실패는 RAG query 실패로 전파하지 않는다.

## Privacy Defaults

- full prompt는 저장하지 않는다.
- full answer는 저장하지 않고 `answer_length`만 기록한다.
- chunk text는 저장하지 않고 `source_path`만 기록한다.
- 질문 원문은 기본 저장하지 않고 `question_hash`만 기록한다.
- `RAG_TRACE_INCLUDE_PREVIEW=true`를 명시한 경우에만 짧은 `question_preview`가 추가된다.

## Smoke Result

trace enabled smoke에서 JSONL event 1건을 확인했다.

- 포함: `schema_version`, `timestamp`, `trace_id`, `route`, `question_hash`, `model`, `top_k`, `retrieved_sources`, `latency_ms`, `answer_length`
- 기본 미포함: `question_preview`, full answer, chunk text

trace disabled smoke에서 `RAG_TRACE_ENABLED=false`일 때 trace file이 생성되지 않는 것을 확인했다.

## Runtime Usage

systemd 서비스에서 활성화하려면 service 환경에 아래 값을 추가한다.

```ini
Environment=RAG_TRACE_ENABLED=true
Environment=RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl
```

적용 후에는 `sudo systemctl daemon-reload`, `sudo systemctl restart ragsystem-api.service` 순서로 재기동한다.

## Next Work

Ubuntu 서버에서 실제 API query와 eval 실행 시 trace가 원하는 경로에 기록되는지 확인한다. 민감 정보가 로그에 포함되지 않는지 운영 로그 샘플로 한 번 더 검증한다.
