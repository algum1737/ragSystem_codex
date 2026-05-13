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

- 구현 변경 승인
- 평가 파이프라인 수정
- full eval 재실행
