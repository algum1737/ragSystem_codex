# 2026-05-14 Retrieval Metric Normalization

## Summary

기존 `precision@k` 계열 지표는 고유 source 수를 `top_k=5`로 나누는 방식이라 relevant source가 2개 또는 4개인 현재 평가셋에서 구조적 상한이 있었다. 검색 품질을 더 정확히 해석하기 위해 기존 지표는 유지하면서 normalized source precision, chunk precision, source recall 지표를 추가했다.

## Changes

- 기존 지표 유지:
  - `precision@k_mean`
  - `vector_precision@k_mean`
  - `rag_precision@k_mean`
  - `source_coverage@k_mean`
- 새 지표 추가:
  - `normalized_source_precision@k_mean`
  - `vector_normalized_source_precision@k_mean`
  - `rag_normalized_source_precision@k_mean`
  - `vector_chunk_precision@k_mean`
  - `rag_chunk_precision@k_mean`
  - `source_recall@k_mean`

## Metric Definitions

| Metric | Definition | Purpose |
| --- | --- | --- |
| `precision@k` | `matched_unique_sources / k` | 기존 리포트 호환 |
| `normalized_source_precision@k` | `matched_unique_sources / min(k, relevant_source_count)` | source 수가 적은 케이스의 상한 보정 |
| `chunk_precision@k` | `matched_retrieved_chunks / k` | top_k context에 비관련 source 청크가 섞이는지 확인 |
| `source_recall@k` | `matched_unique_sources / relevant_source_count` | 관련 source를 모두 포함했는지 확인 |

## Result

- 새 리포트: `eval/results/eval_20260514_164724.json`

| Metric | Value |
| --- | ---: |
| `precision@k_mean` | `0.48` |
| `vector_precision@k_mean` | `0.48` |
| `rag_precision@k_mean` | `0.60` |
| `normalized_source_precision@k_mean` | `0.825` |
| `vector_normalized_source_precision@k_mean` | `0.825` |
| `rag_normalized_source_precision@k_mean` | `1.0` |
| `vector_chunk_precision@k_mean` | `0.98` |
| `rag_chunk_precision@k_mean` | `0.96` |
| `source_recall@k_mean` | `1.0` |
| `source_coverage@k_mean` | `1.0` |
| `accuracy_mean` | `0.90` |
| `faithfulness_mean` | `1.0` |
| `not_found_rate` | `0.0` |

## Interpretation

- 기존 `rag_precision@k_mean=0.60`은 낮은 값이 아니라 기존 metric 설계상 상한이다.
- 새 기준에서는 `rag_normalized_source_precision@k_mean=1.0`, `source_recall@k_mean=1.0`이다.
- RAG 검색 경로는 source 관점에서 현재 평가셋의 관련 source를 모두 포함한다.
- `rag_chunk_precision@k_mean=0.96`이므로 top_k context에 비관련 source 청크가 섞이는 문제도 작다.
- 당장 chunking/query expansion/reranking 튜닝을 적용할 근거는 약하다.

## Remaining Work

- 남은 품질 병목은 검색보다 답변 accuracy 쪽이다.
- 잔여 낮은 accuracy 케이스는 `tc-06`, `tc-07`, `tc-09`다.
- 다음 작업은 expected keyword 정합성 또는 답변 형식 안정성 분석이 적합하다.
