# 2026-06-04 Gemma3 Operating Transition Result

## Summary

운영 응답 기본 모델을 `gemma3:12b + top_k=5`로 전환했다.

`top_k`는 기존 기본값 5를 유지했다. `top_k=3`은 full eval에서 source recall과 accuracy가 회귀했으므로 반영하지 않았다.

## Changed

- `retriever/llm.py`: `DEFAULT_MODEL = "gemma3:12b"`
- `query.py`: CLI 기본 모델을 `gemma3:12b`로 변경
- `app.py`: Streamlit 추천 모델에서 `gemma3:12b`를 운영 기본값으로 표시
- `ARCHITECTURE.md`, `docs/architecture.md`: 생성 스택을 `gemma3:12b`로 변경
- `docs/manual-deployment-guide.md`, `docs/서버_기동_가이드.md`: 기본 모델과 모델 변경 예시를 `gemma3:12b`로 변경

## Server Deployment

변경 파일을 Ubuntu 서버 `/opt/ragSystem_codex`에 반영했다.

서버 compile:

```bash
.venv/bin/python -m py_compile retriever/llm.py query.py api/main.py app.py
```

서버 기본값 확인:

```text
retriever.llm.DEFAULT_MODEL = gemma3:12b
```

## Runtime Transition

전환 전:

```json
{"status":"ok","model":"gemma4:e4b"}
```

전환:

```http
PUT /model {"model":"gemma3:12b"}
```

전환 후:

```json
{"status":"ok","model":"gemma3:12b"}
```

## Smoke Test

대표 질문:

```text
서비스 해지 시 데이터 및 게시물은 어떻게 처리되는가?
```

결과:

- status: 200
- elapsed: about 22.05s
- answer length: 998
- returned sources: 5

Trace:

```json
{
  "route": "api.query",
  "model": "gemma3:12b",
  "top_k": 5,
  "latency_ms": {
    "total": 22045.29,
    "retrieval_total": 136.56,
    "llm": 21908.49
  }
}
```

Ollama state after query:

```text
gemma3:12b  PROCESSOR 100% GPU  CONTEXT 4096
```

## Restart Verification

API process restart 후:

```json
{"status":"ok","model":"gemma3:12b"}
```

Stats:

```json
{"collection_name":"ragSystem","count":318}
```

Streamlit restart 후:

```text
HTTP/1.1 200 OK
```

## Decision

`gemma3:12b + top_k=5`를 현재 운영 기본 조합으로 둔다.

Follow-up candidates:

- 운영 트래픽에서 latency 분포를 더 관찰한다.
- 답변이 길어져 latency가 다시 커지면 `gemma3:12b` 전용 `max_tokens` 제한을 실험한다.
- GPU 메모리 경합이 재발하면 API embedding/reranker CPU 모드 실험을 별도 plan으로 진행한다.
