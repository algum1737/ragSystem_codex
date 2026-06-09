# 2026-06-09 Concise Mode Trace Review

## Summary

운영 trace에서 `answer_mode`가 기록된 `api.query` 이벤트를 확인했다. `standard`와 `concise`가 같은 질문 해시로 짝지어진 표본은 3쌍이며, 모든 표본에서 source 5개가 유지됐다.

결론은 다음과 같다.

- `concise`는 현재 표본에서 답변 길이와 LLM latency를 줄이는 경향이 있다.
- 표본 수가 작고 일부는 retrieval cold load 영향이 있어 운영 기본값을 바꾸거나 자동 라우팅을 도입하기에는 이르다.
- 다음 단계는 concise 전용 경량 평가셋을 추가해 “짧지만 누락 없는 답변” 기준을 고정하는 것이다.

## Environment

- Server: `10.10.220.5`
- Trace path: `/opt/ragSystem_codex/logs/rag_traces.jsonl`
- Route: `api.query`
- Model: `gemma3:12b`
- top_k: `5`

## Trace Counts

전체 `api.query` 성공 이벤트는 29건이었다.

| answer_mode | count | avg total ms | avg LLM ms | avg retrieval ms | avg answer length | avg source count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `concise` | 4 | 8574.29 | 8457.79 | 116.27 | 352.00 | 5.00 |
| `standard` | 3 | 16088.69 | 12737.12 | 3351.35 | 496.00 | 5.00 |
| missing | 22 | 35133.30 | 31912.53 | 3220.51 | 842.91 | 5.00 |

`missing`은 `answer_mode` trace metadata 도입 전 이벤트이므로 이번 판단에서 제외한다.

## Paired Samples

같은 `question_hash`에 대해 `standard`와 `concise`가 모두 있는 표본은 3쌍이다.

| pair | doc_type | mode | total ms | LLM ms | retrieval ms | answer length | source count |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 운영정책 | `standard` | 25248.14 | 15441.22 | 9806.71 | 519 | 5 |
| 1 | 운영정책 | `concise` | 4273.84 | 4164.38 | 109.22 | 230 | 5 |
| 2 | 위치기반서비스 | `standard` | 7120.50 | 7001.26 | 118.99 | 394 | 5 |
| 2 | 위치기반서비스 | `concise` | 6509.92 | 6399.10 | 110.59 | 376 | 5 |
| 3 | 위치기반서비스 | `standard` | 15897.43 | 15768.88 | 128.34 | 575 | 5 |
| 3 | 위치기반서비스 | `concise` | 6166.59 | 6046.29 | 120.07 | 316 | 5 |

Paired sample 평균:

| mode | avg total ms | avg LLM ms | avg answer length | avg source count |
| --- | ---: | ---: | ---: | ---: |
| `standard` | 16088.69 | 12737.12 | 496.33 | 5.00 |
| `concise` | 5650.12 | 5536.59 | 307.33 | 5.00 |

Paired sample 기준 `concise`는 평균 total 약 64.9%, LLM 약 56.5%, answer length 약 38.1%를 줄였다.

## Interpretation

- `concise` source count는 모든 표본에서 5개로 유지됐다.
- `concise` latency 개선은 LLM 구간에서 주로 나타났다.
- 1번 pair는 `standard` 쪽 retrieval이 약 9.8초로 cold load 영향을 받았으므로 total 비교보다 LLM 비교를 우선 본다.
- 2번 pair는 answer length와 latency 차이가 작아, 질문 유형에 따라 concise 이점이 제한적일 수 있다.
- 현재 표본만으로 faithfulness나 누락률을 판단할 수는 없다.

## Decision

`concise`는 선택형 빠른 요약 모드로 유지한다. 운영 기본값 변경, 자동 라우팅, 프롬프트 추가 변경은 보류한다.

다음 작업은 concise 전용 경량 평가셋을 정의하는 것이다. 최소 기준은 다음과 같다.

- 짧은 답변을 요구하는 질의
- 표준 답변 대비 필수 근거 또는 예외사항 누락 여부
- source count와 latency가 함께 남는 trace 기반 smoke
- no-answer 또는 문서 미확인 질문에서 불필요한 확정 표현이 없는지 확인

## Validation

- 운영 API `/health`: `{"status":"ok","model":"gemma3:12b"}`
- 운영 trace 집계: 통과
- 추가 `/query` smoke: 미실행. 최근 post deploy smoke와 trace 표본이 충분해 이번 작업에서는 추가 질의를 만들지 않았다.
