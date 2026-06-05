# 2026-06-04 Speed Improvement Follow-Up Result

## Summary

다음 속도 개선 실행 후보는 `gemma3:12b + top_k=5` 운영 전환이다.

`gemma3:12b + top_k=3`은 latency는 좋았지만 full eval에서 source recall과 accuracy가 회귀했다. `gemma4:e4b`는 현재 운영 API에 설정되어 있으나 full eval 기준선이 없고, 기존 trace에서 `gemma3:12b`보다 빠르지 않았다.

## Current Server State

확인 시점의 서버 상태:

- API `/health`: `{"status":"ok","model":"gemma4:e4b"}`
- `ollama ps`: 상주 모델 없음
- GPU 0: 약 3562 MiB 사용, GPU util 0%
- GPU 1: 약 18 MiB 사용, GPU util 0%

해석:

- 현재 운영 API 모델은 문서상 기본값인 `gemma4:26b`가 아니라 `gemma4:e4b`다.
- Ollama 모델은 상주하지 않아 첫 요청 시 모델 로딩 비용이 붙을 수 있다.
- API Python 프로세스가 GPU 0 메모리를 점유하는 구조는 유지되고 있다.

## Comparison

| Candidate | Quality evidence | Latency evidence | Risk | Decision |
| --- | --- | --- | --- | --- |
| `gemma3:12b + top_k=5` | full eval `accuracy_mean=0.9891`, `faithfulness_mean=0.9565`, `source_recall=1.0` | API trace mean about 23.8s, previous smoke about 29.0s | `tc-07`, `tc-11` gap was observed before but overall full eval is strong | Primary operating candidate |
| `gemma3:12b + top_k=3` | full eval `accuracy_mean=0.942`, `source_recall=0.8449` | eval trace mean about 8.7s | Source recall and answer quality regression | Reject for operating default |
| `gemma4:e4b + top_k=5` | no full eval baseline | API trace mean about 26.1s | `gemma4` family has `num_predict` empty-response risk; not faster than `gemma3:12b` in traces | Do not prioritize |
| `gemma4:26b + top_k=5` | previous operating default | API trace mean about 221.4s | Severe LLM latency; partial CPU offload observed | Keep only as quality-priority/manual option |

## Decision

Proceed with a dedicated operating transition plan for `gemma3:12b + top_k=5`.

This is the lowest-risk speed improvement path because:

- It has an existing full eval baseline.
- It improves latency by roughly an order of magnitude versus `gemma4:26b`.
- It avoids the source recall regression introduced by `top_k=3`.
- It is better supported than `gemma4:e4b`, which lacks full eval coverage.

## Deferred Options

- `top_k=4` experiment: useful only if `gemma3:12b + top_k=5` is still too slow after operating transition.
- API CPU mode for embedding/reranker: useful if keeping a `gemma4` model or if Ollama GPU memory pressure is still a practical issue.
- `gemma3:12b` token cap: useful after transition if response verbosity remains too high.

## Next Work

Create and execute an operating transition plan:

- Confirm whether the user wants API default and runtime model set to `gemma3:12b`.
- Decide whether `top_k=5` remains fixed in code or is exposed as runtime configuration.
- Apply the approved change.
- Verify `/health`, representative `/query`, trace latency, and docs.
