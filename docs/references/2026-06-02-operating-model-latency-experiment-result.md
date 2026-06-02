# 2026-06-02 Operating Model Latency Experiment Result

## Summary

`gemma3:12b`는 운영 API RAG query latency를 크게 줄였지만, full eval에서 기존 `gemma4:26b` 기준선 대비 품질이 소폭 하락했다. 따라서 즉시 운영 기본 모델로 영구 전환하지 않고, 하락 케이스를 먼저 리뷰한다.

## Pre-flight

- 운영 API 초기 모델: `gemma4:26b`
- `gemma3:12b` Ollama model availability 확인 완료
- trace 활성화 확인 완료
- API model change endpoint 검증 중 `RAGEngine.llm` setter 부재를 발견하고 수정했다.

## Fix Applied

`/model` endpoint는 `request.app.state.rag_engine.llm = request.app.state.llm`을 호출하지만, `RAGEngine.query()`는 내부 `_llm`을 사용했다. 이로 인해 `/health`는 바뀌어도 실제 RAG query 모델은 바뀌지 않을 수 있었다.

수정:

- `retriever.engine.RAGEngine.llm` property getter/setter 추가
- 서버 `/opt/ragSystem_codex/retriever/engine.py`에 반영
- 서버 venv compile 확인
- API 프로세스 재기동 후 `/health` 정상 확인

## API Smoke

임시 모델 전환:

```text
PUT /model {"model":"gemma3:12b"}
response: {"model":"gemma3:12b","previous_model":"gemma4:26b"}
health: {"status":"ok","model":"gemma3:12b"}
```

동일 질문 운영 API query trace:

- question: `다음 환불 서비스 정책 알려줘`
- route: `api.query`
- model: `gemma3:12b`
- total: 29032.29 ms
- retrieval_total: 9793.70 ms
- llm: 19238.35 ms
- answer_length: 858

비교 기준 `gemma4:26b` 운영 trace:

- total: 217767.80 ms
- retrieval_total: 9906.41 ms
- llm: 207861.13 ms
- answer_length: 133

Latency 개선:

- total: 약 217.8초 → 약 29.0초
- LLM: 약 207.9초 → 약 19.2초

## Full Eval

Report:

- `eval/results/eval_20260602_131307.json`

Summary:

| metric | `gemma3:12b` |
| --- | ---: |
| total_cases | 23 |
| rag_normalized_source_precision@k_mean | 1.0 |
| source_recall@k_mean | 1.0 |
| accuracy_mean | 0.9891 |
| faithfulness_mean | 0.9565 |
| not_found_success_rate | 1.0 |

기존 안정화 기준선은 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0`이었다. `gemma3:12b`는 latency 개선은 충분하지만 품질 기준선은 완전히 유지하지 못했다.

## Non-perfect Cases

- `tc-07`
  - `answer_accuracy=0.75`
  - `faithfulness=1.0`
  - 위치기반서비스 면책 조항 답변에서 expected keyword 일부 누락.
- `tc-11`
  - `answer_accuracy=1.0`
  - `faithfulness=0.0`
  - 유료서비스 청약철회/환불 제한 조건 답변은 keyword는 맞지만 judge가 근거 충실성을 실패로 판정.

## Runtime Restore

실험 후 운영 API 모델을 원래 상태로 복구했다.

```text
PUT /model {"model":"gemma4:26b"}
response: {"model":"gemma4:26b","previous_model":"gemma3:12b"}
health: {"status":"ok","model":"gemma4:26b"}
```

## Decision

`gemma3:12b`를 즉시 운영 기본 모델로 영구 전환하지 않는다.

다음 작업:

1. `tc-07`, `tc-11` 품질 gap을 리뷰한다.
2. `gemma3:12b`에서 프롬프트 또는 평가셋 보정으로 기준선 회복이 가능한지 확인한다.
3. 기준선 회복 후 운영 기본 모델 변경 여부를 다시 결정한다.
