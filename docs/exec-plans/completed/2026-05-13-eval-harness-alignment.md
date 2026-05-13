# Eval Harness Alignment Plan

## Goal

평가 파이프라인의 retrieval 지표를 실제 RAG 검색 경로와 맞춰, 이후 품질 개선 실험의 판단 기준을 신뢰할 수 있게 만든다.

## Scope

- `eval/pipeline.py`의 vector-only retrieval 지표 명칭 분리
- 실제 `RAGEngine` 최종 source 기준 retrieval 지표 추가
- unique source coverage 지표 추가
- `not_found_rate` 요약 지표 추가
- 전체 eval 재실행과 리포트 저장

## Assumptions

- 현재 RAG 생성 경로는 `RAGEngine.query()`가 기준이다.
- 기존 `precision@k_mean`은 비교를 위해 보존하거나 명칭을 바꿔 병행한다.
- 구현 변경은 사용자 승인 후 진행한다.

## Steps

1. `eval/pipeline.py`의 기존 retrieval metric을 `vector_precision@k`로 분리한다.
2. `RAGEngine.query()` 결과의 `sources`로 `rag_precision@k`를 계산한다.
3. relevant source 기준 unique coverage를 `source_coverage@k`로 계산한다.
4. 답변이 `찾을 수 없음`인 비율을 `not_found_rate`로 요약한다.
5. `python eval/pipeline.py --all`을 실행해 새 리포트를 저장한다.

## Risks

- `RAGEngine.query()`는 LLM 호출을 포함하므로 retrieval-only보다 느리고 Ollama 상태에 영향을 받는다.
- 기존 리포트와 필드명이 달라지면 과거 비교 스크립트가 필요할 수 있다.

## Validation

- `bash scripts/validate-docs.sh`가 통과해야 한다.
- `.venv/bin/python eval/pipeline.py --all`이 새 지표를 포함한 리포트를 저장해야 한다.
- 새 리포트에 `vector_precision@k`, `rag_precision@k`, `source_coverage@k`, `not_found_rate`가 포함되어야 한다.

## Open Work

- 없음

## Progress

- `eval/pipeline.py`의 기존 vector-only precision을 `vector_precision_at_k`로 분리했다.
- 기존 `precision_at_k`와 `retrieved_sources`는 과거 리포트 소비 코드 호환을 위해 alias로 유지했다.
- 실제 `RAGEngine.query()` 결과 source 기준 `rag_precision_at_k`를 추가했다.
- relevant source의 unique coverage를 보는 `source_coverage_at_k`를 추가했다.
- 답변의 `찾을 수 없습니다` 포함 여부를 요약하는 `not_found`와 `not_found_rate`를 추가했다.
- full eval을 재실행해 새 리포트를 저장했다.

## Verification Notes

- `.venv/bin/python -m py_compile eval/pipeline.py` 통과
- `bash scripts/validate-docs.sh` 통과
- `.venv/bin/python eval/pipeline.py --all` 통과
- 최신 리포트: `eval/results/eval_20260513_134658.json`
- 최신 지표:
  - `precision@k_mean: 0.48`
  - `vector_precision@k_mean: 0.48`
  - `rag_precision@k_mean: 0.54`
  - `source_coverage@k_mean: 0.925`
  - `accuracy_mean: 0.625`
  - `faithfulness_mean: 0.8`
  - `not_found_rate: 0.2`

## Completion

- 완료일: 2026-05-13
- retrieval 평가 지표와 실제 RAG 검색 경로를 분리해서 계측할 수 있게 했다.
- 다음 품질 개선 판단 기준은 `rag_precision@k`, `source_coverage@k`, `not_found_rate`를 함께 본다.
- 남은 작업 없음.
