# 2026-06-09 Selective Concise Answer Mode Result

## Summary

기본 RAG 프롬프트를 유지하면서, 사용자가 명시적으로 선택할 때만 concise prompt를 사용하는 `answer_mode`를 구현했다.

결론:

- 기본값은 `standard`다.
- `standard`는 기존 `PROMPT_TEMPLATE`를 그대로 사용한다.
- `concise`는 `CONCISE_PROMPT_TEMPLATE`를 per-call로 선택한다.
- 요청 중 module-level prompt를 변경하지 않으므로 동시 요청 간 prompt 경합이 없다.
- 서버 API/Web에 반영했고 `/health`, Streamlit health, API smoke, standard full eval을 확인했다.

## Implementation

변경 사항:

- `retriever/engine.py`
  - `CONCISE_PROMPT_TEMPLATE` 추가
  - `ANSWER_MODE_PROMPTS` 추가
  - `RAGEngine.query(answer_mode="standard")` 추가
  - trace metadata에 `answer_mode` 기록
- `api/models.py`
  - `QueryRequest.answer_mode` 추가
  - 허용 값: `standard`, `concise`
- `api/main.py`
  - `/query`에서 `answer_mode`를 `RAGEngine.query()`에 전달
- `query.py`
  - `--answer-mode standard|concise` 옵션 추가
- `app.py`
  - Query UI에 `표준`/`빠른 요약` 답변 모드 선택 추가

## Server Deployment

- Server: Ubuntu server `10.10.220.5`
- API: `ragsystem-api`
- Web: `ragsystem-web`
- Model: `gemma3:12b`

검증:

- 서버 compile 통과:
  - `.venv/bin/python -m py_compile retriever/engine.py api/models.py api/main.py query.py app.py`
- API/Web 재기동 확인:
  - `systemctl is-active ragsystem-api ragsystem-web` -> `active`, `active`
  - `/health` -> `{"status":"ok","model":"gemma3:12b"}`
  - Streamlit `_stcore/health` -> `ok`

## API Smoke

### 운영정책

Question:

`운영정책에서 계정 이용이 제한되거나 해지될 수 있는 조건은 무엇인가?`

| mode | elapsed ms | trace total ms | trace LLM ms | answer length |
|---|---:|---:|---:|---:|
| standard | 25253.94 | 25248.14 | 15441.22 | 519 |
| concise | 4278.37 | 4273.84 | 4164.38 | 230 |

Note:

- `standard`는 API/Web 재시작 직후 첫 호출이라 embedding/rerank cold load가 포함됐다.
- warmed 상태의 `concise`는 짧은 bullet 형식으로 정상 응답했다.

### 위치기반서비스

Question:

`위치기반서비스 약관에서 개인위치정보는 어떤 목적으로 이용되는가?`

| mode | elapsed ms | trace total ms | trace LLM ms | answer length |
|---|---:|---:|---:|---:|
| standard | 7125.52 | 7120.50 | 7001.26 | 394 |
| concise | 6513.46 | 6509.92 | 6399.10 | 376 |

Note:

- 이 케이스에서는 concise가 항상 크게 빠르지는 않았다.
- 선택형 모드는 편의 기능이며, 모든 질문에서 속도 개선을 보장하지 않는다.

## Trace

최신 API smoke trace는 `/opt/ragSystem_codex/logs/rag_traces.jsonl`에 기록됐다.

`metadata.answer_mode`:

- `standard`
- `concise`

## Full Eval

기본 `standard` 경로가 기존 품질 기준선을 유지하는지 확인하기 위해 서버 full eval을 실행했다.

Command:

```bash
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/opt/ragSystem_codex/logs/selective_concise_standard_eval_20260609.jsonl \
.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
```

Report:

`/opt/ragSystem_codex/eval/results/eval_20260609_110223.json`

Summary:

| metric | value |
|---|---:|
| total_cases | 23 |
| rag_normalized_source_precision@k_mean | 1.0 |
| source_recall@k_mean | 1.0 |
| accuracy_mean | 0.9891 |
| faithfulness_mean | 0.9565 |
| not_found_success_rate | 1.0 |

## Decision

선택형 concise answer mode를 구현 상태로 유지한다.

운영 기본값은 `standard`이며 full eval 기준선을 유지했다. `concise`는 사용자가 빠른 요약 답변을 명시적으로 선택할 때만 사용한다.

## Remaining Work

- 변경분 커밋
- 필요 시 원격 push
- 사용자가 원하면 concise mode에 대한 추가 대표 질문 smoke 확장
