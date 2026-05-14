# Next Search Quality Experiment Plan

## Goal

평가셋 정합성 보정 이후 남은 검색 지표 병목을 분석하고, 다음 검색 품질 개선 실험을 하나로 좁힌다.

## Scope

- 최신 리포트 `eval/results/eval_20260514_152044.json` 기준 검색 실패/부분 실패 케이스 확인
- chunking, query expansion, reranking threshold, source diversity 전략 비교
- 구현 전 실험 후보와 검증 기준 정리

## Out Of Scope

- 즉시 구현 변경
- Ollama 모델 교체
- 외부 API 평가 도입
- 평가셋 keyword 추가 보정

## Assumptions

- 최신 기준선은 `eval/results/eval_20260514_152044.json`이다.
- 현재 검색 지표는 `precision@k_mean=0.48`, `vector_precision@k_mean=0.48`, `rag_precision@k_mean=0.60`, `source_coverage@k_mean=1.0`이다.
- 다음 구현 변경은 사용자 승인 이후에만 수행한다.

## Pre-flight checks

- `main`과 `origin/main` 동기화 확인
- 최신 full eval 리포트 확인
- `eval/test_cases.json`의 expected sources와 retrieved sources 대조

## Steps

1. 최신 full eval의 케이스별 retrieval 결과를 분석한다.
2. 낮은 precision 케이스를 원인별로 분류한다.
3. chunking, query expansion, reranking threshold, source diversity 조정 후보를 비교한다.
4. 사용자 승인 후 별도 구현 계획으로 승격한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- 구현 승격 시 `.venv/bin/python eval/pipeline.py --metric retrieval`
- 구현 승격 시 `.venv/bin/python eval/pipeline.py --all`

## Manual/Runtime QA

- 검색 지표 하락 없이 `precision@k_mean` 개선 가능성이 있는지 케이스별 source를 직접 대조한다.
- `source_coverage@k_mean=1.0`을 유지할 수 있는 후보를 우선한다.

## Skipped/Not Run

- 구현 전 계획이므로 검색 튜닝 실험과 full eval 재실행은 아직 실행하지 않는다.

## Validation Result

- 통과: 최신 full eval 리포트 확인
  - `eval/results/eval_20260514_152044.json`
- 통과: 케이스별 relevant source 수와 RAG precision 상한 분석
  - 2-source 케이스 5개 최고점: `0.4`
  - 4-source 케이스 5개 최고점: `0.8`
  - 현 metric 기준 전체 평균 상한: `0.60`
- 통과: 현재 RAG 검색 결과 대조
  - 모든 케이스 `source_coverage_at_k=1.0`
  - 모든 케이스가 현 `rag_precision_at_k` 상한 도달
- 통과: 검색 튜닝 후보 비교
  - chunking, query expansion, reranking threshold/window, source diversity 추가 튜닝은 현재 지표 기준 즉시 효과 제한
- 결정: 다음 구현 후보는 retrieval metric normalization
  - 분석 문서: `docs/references/2026-05-14-search-quality-ceiling-analysis.md`

## Open Work

- 없음.

## Completion

- 완료: 최신 retrieval 실패/부분 실패 케이스 분석
- 완료: 현 `rag_precision@k_mean=0.60`이 metric 상한임을 확인
- 완료: 다음 구현 후보를 retrieval metric normalization으로 선정
