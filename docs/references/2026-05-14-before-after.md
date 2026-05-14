# 2026-05-14 Before After

## Scope

이 문서는 검색 품질 개선 전후의 지표 차이를 기록한다.

- Before: `eval/results/eval_20260513_164755.json`
- After: `eval/results/eval_20260514_113849.json`

## Summary Metrics

| Metric | Before | After | Delta | Note |
| --- | ---: | ---: | ---: | --- |
| `precision@k_mean` | `0.48` | `0.48` | `0.00` | vector-only 호환 지표 |
| `vector_precision@k_mean` | `0.48` | `0.48` | `0.00` | 순수 벡터 검색은 변경하지 않음 |
| `rag_precision@k_mean` | `0.54` | `0.60` | `+0.06` | 실제 RAG 최종 source 지표 개선 |
| `source_coverage@k_mean` | `0.925` | `1.0` | `+0.075` | 관련 source coverage 완전 충족 |
| `accuracy_mean` | `0.675` | `0.70` | `+0.025` | 답변 키워드 매칭 소폭 개선 |
| `faithfulness_mean` | `0.8` | `0.9` | `+0.1` | 근거성 판정 개선 |
| `not_found_rate` | `0.1` | `0.1` | `0.0` | no-answer 비율 유지 |

## Case-Level Changes

| Case | `rag_precision@k` Before | `rag_precision@k` After | `source_coverage@k` Before | `source_coverage@k` After | `accuracy` Before | `accuracy` After | `faithfulness` Before | `faithfulness` After |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `tc-01` | `0.4` | `0.4` | `1.0` | `1.0` | `0.0` | `0.0` | `0.0` | `0.0` |
| `tc-02` | `0.8` | `0.8` | `1.0` | `1.0` | `1.0` | `1.0` | `1.0` | `1.0` |
| `tc-03` | `0.4` | `0.4` | `1.0` | `1.0` | `0.5` | `0.5` | `1.0` | `1.0` |
| `tc-04` | `0.4` | `0.8` | `0.5` | `1.0` | `0.25` | `0.25` | `1.0` | `1.0` |
| `tc-05` | `0.4` | `0.4` | `1.0` | `1.0` | `1.0` | `1.0` | `1.0` | `1.0` |
| `tc-06` | `0.8` | `0.8` | `1.0` | `1.0` | `0.75` | `0.75` | `1.0` | `1.0` |
| `tc-07` | `0.6` | `0.8` | `0.75` | `1.0` | `1.0` | `1.0` | `1.0` | `1.0` |
| `tc-08` | `0.8` | `0.8` | `1.0` | `1.0` | `1.0` | `1.0` | `1.0` | `1.0` |
| `tc-09` | `0.4` | `0.4` | `1.0` | `1.0` | `0.5` | `0.75` | `1.0` | `1.0` |
| `tc-10` | `0.4` | `0.4` | `1.0` | `1.0` | `0.75` | `0.75` | `0.0` | `1.0` |

## Interpretation

- `vector_precision@k_mean`은 그대로다. 이번 변경은 Chroma vector-only 검색이 아니라 실제 RAG 최종 검색 경로를 개선했다.
- `rag_precision@k_mean`은 `tc-04`, `tc-07`에서 source 다양성 보존 효과로 개선됐다.
- `source_coverage@k_mean`은 `1.0`에 도달했다. 관련 source가 최종 RAG context에 모두 포함되는 상태다.
- `tc-01`은 여전히 낮다. 현재 문서 기준으로 환불 정책 근거가 약하거나 평가 질문과 문서 근거가 맞지 않을 가능성이 높다.
- 다음 작업은 `tc-01`, `tc-03`, `tc-04`, `tc-09`를 중심으로 답변 품질과 평가셋 정합성을 다시 분류하는 것이다.
