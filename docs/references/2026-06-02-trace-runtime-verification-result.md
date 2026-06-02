# 2026-06-02 Trace Runtime Verification Result

## Server

- Host: `10.10.220.5`
- User: `ragadmin`
- App path: `/opt/ragSystem_codex`
- API service: `ragsystem-api.service`
- Web service: `ragsystem-web.service`

## Completed

- SSH 접근 확인: `srv01`
- 운영 API 상태 확인: `ragsystem-api.service` active
- 운영 API health 확인: `{"status":"ok","model":"gemma4:26b"}`
- 최신 trace 코드 배포:
  - local tarball을 `/home/ragadmin/ragSystem_codex-trace-runtime.tar.gz`로 업로드
  - `/opt`에 압축 해제
  - `/opt/ragSystem_codex/observability/trace.py` 존재 확인
- 서버 venv compile 확인:
  - `.venv/bin/python -m py_compile api/main.py retriever/engine.py eval/pipeline.py query.py observability/trace.py`
- 임시 API trace smoke:
  - `127.0.0.1:8010`에 `RAG_TRACE_ENABLED=true`로 임시 API 기동
  - `/health` 정상
  - `/query` 1건 실행 후 `/opt/ragSystem_codex/logs/rag_traces_runtime_smoke.jsonl` 생성 확인
  - trace route: `api.query`
  - 기본 미포함 확인: full answer, question preview, chunk text
- eval trace smoke:
  - `RAG_TRACE_ENABLED=true RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces_eval_smoke.jsonl .venv/bin/python eval/pipeline.py --metric retrieval --top-k 5`
  - eval status: `0`
  - trace count: `23`
  - last route: `eval.case`
  - last case: `tc-23`
  - score keys recorded: `precision_at_k`, `rag_precision_at_k`, `rag_normalized_source_precision_at_k`, `source_recall_at_k`, `answer_accuracy`, `faithfulness`, `not_found_success`
  - 기본 미포함 확인: full answer, question preview, chunk text

## Observed Runtime

임시 API query에서 `gemma4:26b` LLM 구간이 약 351초로 측정됐다.

- `embedding`: 8205.13 ms
- `vector_search`: 182.80 ms
- `bm25_search`: 54.68 ms
- `rerank`: 1314.12 ms
- `retrieval_total`: 9757.04 ms
- `llm`: 351265.87 ms
- `total`: 361023.27 ms

검색/임베딩/rerank는 정상 동작했으며, 지연의 대부분은 Ollama LLM 생성 구간이다.

## Pending

systemd service에 `RAG_TRACE_ENABLED`와 `RAG_TRACE_PATH`를 적용하는 작업은 `sudo` 비밀번호가 필요해 완료하지 못했다. 운영 API 서비스 자체는 active 상태로 유지했다.

서버에는 적용 스크립트를 업로드했다.

- local script: `scripts/apply-trace-systemd.sh`
- server script: `/home/ragadmin/apply-ragsystem-trace.sh`

사용자가 서버에서 아래를 실행해야 systemd API 서비스 trace가 켜진다.

```bash
sudo bash /home/ragadmin/apply-ragsystem-trace.sh
```

수동으로 적용하려면 아래 절차를 사용한다.

```bash
sudo systemctl edit ragsystem-api.service
```

에디터에 아래 내용을 입력한다.

```ini
[Service]
Environment=RAG_TRACE_ENABLED=true
Environment=RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl
```

적용한다.

```bash
sudo systemctl daemon-reload
sudo systemctl restart ragsystem-api.service
sudo systemctl status ragsystem-api.service
curl http://localhost:8000/health
```

query 후 확인한다.

```bash
tail -n 5 /opt/ragSystem_codex/logs/rag_traces.jsonl
```
