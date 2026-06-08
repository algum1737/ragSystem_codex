# 2026-06-05 Gemma3 Token Cap Experiment Result

## Summary

`gemma3:12b` 전용 기본 token cap은 채택하지 않는다.

낮은 cap은 latency를 줄였지만 답변 절단 또는 keyword accuracy 회귀가 있었다. 높은 cap은 답변 완결성은 유지했지만 latency 개선이 거의 없었다.

## Candidates

대표 질의:

- `tc-01`: 서비스 해지 시 데이터 및 게시물 처리
- `tc-18`: 위치기반서비스 개인위치정보 이용 목적
- `tc-22`: 운영정책 계정 이용 제한/해지 조건

| Cap | Result |
| ---: | --- |
| 128 | 빠르지만 `tc-22` keyword accuracy가 0.75로 회귀하고 답변 절단 징후가 있었다. |
| 256 | keyword accuracy는 대체로 유지됐지만 긴 답변과 위치기반서비스 답변에서 절단 징후가 있었다. |
| 384 | keyword accuracy는 유지됐지만 세 대표 질의 모두 답변 절단 징후가 있었다. |
| 512 | `tc-18`, `tc-22`는 완결됐지만 긴 `tc-01`은 절단됐다. |
| 768 | 긴 `tc-01` 직접 호출은 완결됐지만 API 기본 cap 적용 후 긴 답변에서 끝부분 불완전성이 남았다. |
| 1024 | 답변 완결성은 회복됐지만 대표 API query latency가 기존 uncapped와 비슷해 실익이 작았다. |

## Key Observations

- 128/256/384는 운영 기본값으로 너무 낮다.
- 512도 긴 답변에는 부족하다.
- 768은 단건 직접 호출에서는 가능성이 있었지만 API 경로에서는 안정적인 하한으로 보기 어렵다.
- 1024는 절단 리스크를 줄이나 latency 개선이 작다.

API trace examples after temporary 768 cap:

- 긴 해지/데이터 query: total 약 20.6초, retrieval 약 9.8초, LLM 약 10.7초, answer length 957
- 위치기반서비스 query: total 약 12.6초, LLM 약 12.5초, answer length 835
- 운영정책 query: total 약 7.8초, LLM 약 7.7초, answer length 625

1024 cap examples:

- 긴 해지/데이터 query: elapsed 약 22.65초, answer length 1085, 완결
- 운영정책 query: elapsed 약 9.09초, answer length 722, 완결

## Decision

Do not set a default `num_predict`/`max_tokens` cap.

The current default remains:

- model: `gemma3:12b`
- `top_k`: 5
- no default token cap

## Rollback

The temporary code change that applied a default cap to `gemma3:12b` was removed locally and on the server.

Server verification:

```text
DEFAULT_MODEL=gemma3:12b
default token cap: none
/health: {"status":"ok","model":"gemma3:12b"}
```

## Next Work

The next practical step is to wrap up the operating transition branch:

- review changed files
- decide whether to commit and open a PR
- keep later tuning candidates separate

Deferred tuning candidates:

- concise-answer prompt experiment
- API embedding/reranker warm-up or CPU-mode experiment
- `top_k=4` only if quality/speed trade-off is reopened
