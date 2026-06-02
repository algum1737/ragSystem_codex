# 2026-06-02 LLM Latency Triage Result

## Summary

운영 지연의 주 원인은 retrieval이 아니라 Ollama LLM 생성 구간이다. `gemma4:26b`는 운영 RAG query에서 LLM만 208초 이상 걸렸고, 같은 RAG 경로를 `gemma3:12b`로 실행하면 LLM 구간이 약 16.5초로 줄었다.

## Runtime Evidence

### Operating API Trace

운영 API `/query` trace:

- model: `gemma4:26b`
- total: 217767.80 ms
- retrieval_total: 9906.41 ms
- llm: 207861.13 ms
- answer_length: 133
- route: `api.query`

임시 API trace에서도 같은 경향이 확인됐다.

- model: `gemma4:26b`
- total: 361023.27 ms
- retrieval_total: 9757.04 ms
- llm: 351265.87 ms

### GPU And Ollama State

측정 중 `ollama ps`는 `gemma4:26b`를 아래처럼 표시했다.

```text
gemma4:26b  SIZE 20 GB  PROCESSOR 15%/85% CPU/GPU  CONTEXT 4096
```

서버 GPU는 11GB급 2장이다. Ollama는 GPU를 사용하지만 `gemma4:26b`는 일부 CPU offload가 발생한다.

### Controlled Ollama Generate

짧은 prompt, `num_predict=64` 기준:

| model | elapsed | load | prompt eval | eval | note |
| --- | ---: | ---: | ---: | ---: | --- |
| `gemma3:12b` | 8.61s | 7.96s | 0.05s | 0.47s | 정상 응답 |
| `gemma4:e4b` | 14.38s | 13.23s | 0.04s | 0.72s | 응답 preview 비어 있음 |
| `gemma4:26b` | 15.69s | 11.89s | 0.25s | 3.18s | 응답 preview 비어 있음 |

RAG 유사 긴 context, `num_predict=64` 기준:

| model | context chars | elapsed | prompt eval | eval | response |
| --- | ---: | ---: | ---: | ---: | --- |
| `gemma4:26b` | 1000 | 12.84s | 0.40s | 2.53s | 빈 응답 |
| `gemma4:26b` | 4000 | 4.07s | 0.93s | 2.59s | 빈 응답 |
| `gemma4:26b` | 8000 | 5.47s | 2.00s | 2.85s | 정상 응답 |
| `gemma3:12b` | 8000 | 15.90s | 2.54s | 1.22s | 정상 응답 |

### LangChain Ollama Path

현재 앱과 같은 `OllamaLLM.predict()` 경로:

| model | max_tokens | elapsed | result |
| --- | ---: | ---: | --- |
| `gemma4:26b` | none | 37.13s | 정상 응답 |
| `gemma4:26b` | 64 | 3.25s | 빈 응답 오류 |
| `gemma4:26b` | 256 | 11.70s | 빈 응답 오류 |
| `gemma3:12b` | none | 14.21s | 정상 응답 |
| `gemma3:12b` | 64 | 1.43s | 정상 응답 |
| `gemma3:12b` | 256 | 2.12s | 정상 응답 |
| `gemma4:e4b` | none | 21.24s | 정상 응답 |
| `gemma4:e4b` | 64 | 1.16s | 정상 응답 |
| `gemma4:e4b` | 256 | 3.68s | 빈 응답 오류 |

`gemma4` 계열은 `num_predict` 제한을 적용하면 빈 응답이 발생할 수 있으므로 단순 max token cap 패치는 위험하다.

### RAG Path Comparison

서버 CLI로 같은 RAGEngine 경로를 `gemma3:12b`로 실행했다.

- route: `cli.query`
- model: `gemma3:12b`
- total: 26285.80 ms
- retrieval_total: 9759.12 ms
- llm: 16526.54 ms
- answer_length: 473
- full answer/question preview 미저장 확인

같은 유형의 운영 API `gemma4:26b` trace와 비교하면:

| model | total | retrieval | llm |
| --- | ---: | ---: | ---: |
| `gemma4:26b` | 217.8s | 9.9s | 207.9s |
| `gemma3:12b` | 26.3s | 9.8s | 16.5s |

## Findings

1. Retrieval path는 주 병목이 아니다.
   - embedding, vector search, BM25, rerank 합계는 약 10초다.
2. `gemma4:26b` 운영 지연은 LLM 생성 구간에서 발생한다.
3. `gemma4:26b`는 GPU를 사용하지만 일부 CPU offload가 발생한다.
4. 현재 LangChain Ollama 경로에서 `gemma4` 계열에 `num_predict`를 단순 적용하면 빈 응답 리스크가 있다.
5. `gemma3:12b`는 같은 RAG 경로에서 훨씬 빠르고 `max_tokens` 제한도 정상 동작한다.

## Recommendation

1차 운영 개선 후보는 운영 기본 모델을 `gemma3:12b`로 낮추고 품질 기준선을 재검증하는 것이다.

보조 후보:

- `gemma3:12b` 전용 `max_tokens` 제한 실험
- `top_k=5` 유지 후 `max_context_chars`만 줄이는 실험
- `gemma4:26b`는 품질 우선 모드로 남기되 기본 운영 모델에서 제외하는 방안

## Next Work

운영 모델 변경은 품질 평가와 함께 진행해야 한다. 다음 plan은 `gemma3:12b` 운영 모델 전환 실험과 full eval 재검증으로 잡는다.
