# 2026-05-14 Search Quality Ceiling Analysis

## Summary

평가셋 정합성 보정 이후 다음 검색 품질 실험 후보를 분석했다. 결론은 검색 튜닝보다 **retrieval metric 재정의가 우선**이다.

현재 `rag_precision@k_mean=0.60`은 낮아 보이지만, 현 평가 방식에서는 사실상 상한에 도달한 값이다. `precision_at_k()`가 중복 청크를 세지 않고 고유 source만 집계한 뒤 `top_k=5`로 나누기 때문이다.

## Current Baseline

- 최신 리포트: `eval/results/eval_20260514_152044.json`
- `precision@k_mean`: `0.48`
- `vector_precision@k_mean`: `0.48`
- `rag_precision@k_mean`: `0.60`
- `source_coverage@k_mean`: `1.0`
- `accuracy_mean`: `0.875`
- `faithfulness_mean`: `1.0`
- `not_found_rate`: `0.0`

## Metric Ceiling

현재 `precision_at_k()`는 아래 방식으로 계산된다.

```text
unique(retrieved_sources[:k]) ∩ relevant_sources / k
```

따라서 `top_k=5`일 때 relevant source가 2개인 케이스의 최고점은 `2 / 5 = 0.4`이고, relevant source가 4개인 케이스의 최고점은 `4 / 5 = 0.8`이다.

| Case Group | Cases | Relevant Sources | Max Current Precision |
| --- | --- | ---: | ---: |
| 2-source cases | `tc-01`, `tc-03`, `tc-05`, `tc-09`, `tc-10` | 2 | 0.4 |
| 4-source cases | `tc-02`, `tc-04`, `tc-06`, `tc-07`, `tc-08` | 4 | 0.8 |

전체 평균 상한은 아래와 같다.

```text
((5 cases * 0.4) + (5 cases * 0.8)) / 10 = 0.60
```

즉 현재 `rag_precision@k_mean=0.60`은 현 metric 기준 이론상 최고점이다.

## Case Review

| Case | RAG Precision | Source Coverage | Interpretation |
| --- | ---: | ---: | --- |
| `tc-01` | 0.4 | 1.0 | 2-source 케이스의 상한 도달 |
| `tc-02` | 0.8 | 1.0 | 4-source 케이스의 상한 도달 |
| `tc-03` | 0.4 | 1.0 | 2-source 케이스의 상한 도달 |
| `tc-04` | 0.8 | 1.0 | 4-source 케이스의 상한 도달 |
| `tc-05` | 0.4 | 1.0 | 2-source 케이스의 상한 도달 |
| `tc-06` | 0.8 | 1.0 | 4-source 케이스의 상한 도달 |
| `tc-07` | 0.8 | 1.0 | 4-source 케이스의 상한 도달 |
| `tc-08` | 0.8 | 1.0 | 4-source 케이스의 상한 도달 |
| `tc-09` | 0.4 | 1.0 | RAG 경로는 상한 도달, vector-only는 0.2 |
| `tc-10` | 0.4 | 1.0 | 2-source 케이스의 상한 도달 |

## Candidate Comparison

| Candidate | Expected Impact Now | Risk | Decision |
| --- | --- | --- | --- |
| Chunking change | 낮음 | DB 재인제스천 필요, 기존 coverage 회귀 가능 | 보류 |
| Query expansion | 낮음~중간 | off-topic source 증가 가능 | 보류 |
| Reranking threshold/window | 낮음 | RAG 지표는 이미 상한, 답변 context 흔들림 가능 | 보류 |
| Source diversity 추가 튜닝 | 낮음 | 현재 `source_coverage=1.0`이므로 이득 제한 | 보류 |
| Retrieval metric normalization | 높음 | 기존 리포트와 비교 방식 변경 필요 | 우선 |

## Recommended Next Work

다음 구현 후보는 **retrieval metric normalization**이다.

권장 변경:

- 기존 `precision@k_mean` / `rag_precision@k_mean`은 backward-compatible하게 유지한다.
- 새 지표를 추가한다.
  - `source_recall@k`: 현재 `source_coverage@k`와 같은 의미를 더 명확한 이름으로 제공
  - `normalized_source_precision@k`: `matched_unique_sources / min(k, relevant_source_count)`
  - `chunk_precision@k`: top_k 청크 각각이 relevant source에서 왔는지 비율로 평가
- 문서에는 기존 precision의 상한 문제를 명시한다.

## Decision

검색 튜닝 구현으로 바로 가는 것은 비효율적이다. 현재 검색 경로는 평가셋 source coverage 기준으로 이미 모든 관련 source를 포함한다. 다음 작업은 metric을 명확히 분리해 앞으로의 검색 실험이 실제로 개선 가능한 대상을 측정하도록 만드는 것이다.
