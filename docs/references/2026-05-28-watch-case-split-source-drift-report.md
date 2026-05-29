# Source Drift Report

## Summary

- `total_cases`: `22`
- `accuracy_mean`: `1.0000`
- `faithfulness_mean`: `1.0000`
- `not_found_success_rate`: `1.0000`
- `rag_normalized_source_precision@k_mean`: `0.9795`
- `source_recall@k_mean`: `0.9692`

## Critical Cases

- 없음.

## Watch Cases

| Case | Recall | RAG Precision | Accuracy | Faithfulness | Missing Relevant Sources | Unexpected RAG Sources |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| tc-06 | 0.5714 | 0.8000 | 1.0000 | 1.0000 | 네이버 위치기반서비스 이용약관.txt, 네이버 이용약관.txt, 다음 위치기반서비스 이용약관.txt | 카카오 운영정책.txt |

## Thresholds

- critical source recall: `< 0.5000`
- critical rag normalized source precision: `< 0.5000`
- watch source recall: `< 0.7500`
- watch rag normalized source precision: `< 0.7500`
