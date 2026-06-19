# Source Drift Report

## Summary

- `total_cases`: `32`
- `accuracy_mean`: `0.9875`
- `faithfulness_mean`: `1.0000`
- `not_found_success_rate`: `1.0000`
- `rag_normalized_source_precision@k_mean`: `1.0000`
- `source_recall@k_mean`: `1.0000`

## Critical Cases

| Case | Recall | RAG Precision | Accuracy | Faithfulness | Missing Relevant Sources | Unexpected RAG Sources |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| tc-30 | 1.0000 | 1.0000 | 0.6000 | 1.0000 | - | - |

## Watch Cases

- 없음.

## Thresholds

- critical source recall: `< 0.5000`
- critical rag normalized source precision: `< 0.5000`
- watch source recall: `< 0.7500`
- watch rag normalized source precision: `< 0.7500`
