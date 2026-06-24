# Source Drift Report

## Summary

- `total_cases`: `39`
- `accuracy_mean`: `0.9711`
- `faithfulness_mean`: `1.0000`
- `not_found_success_rate`: `1.0000`
- `rag_normalized_source_precision@k_mean`: `1.0000`
- `source_recall@k_mean`: `1.0000`

## Critical Cases

| Case | Recall | RAG Precision | Accuracy | Faithfulness | Missing Relevant Sources | Unexpected RAG Sources |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| tc-07 | 1.0000 | 1.0000 | 0.7500 | 1.0000 | - | - |
| tc-28 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | - | 게시물 운영정책.txt, 카카오 운영정책.txt |
| tc-29 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | - | - |
| tc-34 | 1.0000 | 1.0000 | 0.6667 | 1.0000 | - | - |
| tc-37 | 1.0000 | 1.0000 | 0.8571 | 1.0000 | - | 카카오 유료:결제서비스 이용약관.txt |

## Watch Cases

- 없음.

## Thresholds

- critical source recall: `< 0.5000`
- critical rag normalized source precision: `< 0.5000`
- watch source recall: `< 0.7500`
- watch rag normalized source precision: `< 0.7500`
