# Source Drift Report

## Summary

- `total_cases`: `17`
- `accuracy_mean`: `1.0000`
- `faithfulness_mean`: `1.0000`
- `not_found_success_rate`: `1.0000`
- `rag_normalized_source_precision@k_mean`: `0.7971`
- `source_recall@k_mean`: `0.7836`

## Critical Cases

- 없음.

## Watch Cases

| Case | Recall | RAG Precision | Accuracy | Faithfulness | Missing Relevant Sources | Unexpected RAG Sources |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| tc-02 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 네이버 위치기반서비스 이용약관.txt, 다음 위치기반서비스 이용약관.txt | 카카오 위치정보 이용약관.txt, 카카오계정약관20240416.pdf, 카카오통합서비스약관20210701.pdf |
| tc-03 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 다음 이용약관.txt | 게시물 운영정책.txt, 계정 운영정책.txt, 다음 위치기반서비스 이용약관.txt, 카카오 운영정책.txt |
| tc-06 | 0.5714 | 0.8000 | 1.0000 | 1.0000 | 네이버 위치기반서비스 이용약관.txt, 네이버 이용약관.txt, 다음 위치기반서비스 이용약관.txt | 카카오 운영정책.txt |
| tc-07 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 네이버 위치기반서비스 이용약관.txt, 다음 이용약관.txt | 계정 운영정책.txt, 네이버 유료서비스 이용약관.txt, 카카오 위치정보 이용약관.txt |
| tc-08 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 네이버 이용약관.txt, 다음 이용약관.txt | 카카오 위치정보 이용약관.txt, 카카오 유료:결제서비스 이용약관.txt, 카카오계정약관20240416.pdf |
| tc-14 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 계정 운영정책.txt | 네이버 이용약관.txt, 다음 이용약관.txt, 카카오 운영정책.txt, 카카오 유료:결제서비스 이용약관.txt |
| tc-15 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 네이버 이용약관.txt, 카카오 서비스 약관_20260221_F.pdf | 다음 위치기반서비스 이용약관.txt, 카카오 유료:결제서비스 이용약관.txt, 카카오계정약관20240416.pdf |

## Thresholds

- critical source recall: `< 0.5000`
- critical rag normalized source precision: `< 0.5000`
- watch source recall: `< 0.7500`
- watch rag normalized source precision: `< 0.7500`
