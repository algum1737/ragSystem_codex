# Retrieval Metric Normalization Plan

## Goal

현재 `precision@k` 계열 지표의 상한 문제를 보정하고, 검색 품질 실험이 실제 개선 가능 대상을 측정하도록 retrieval metric을 분리한다.

## Scope

- `eval/pipeline.py`에 normalized source precision과 chunk precision 계열 지표 추가
- 기존 `precision@k_mean`, `vector_precision@k_mean`, `rag_precision@k_mean`은 backward-compatible하게 유지
- 새 리포트 생성 및 기존 기준선과 비교
- 문서와 handoff 갱신

## Out Of Scope

- 검색 알고리즘 튜닝
- 청킹/인제스천 구조 변경
- Ollama 모델 교체
- 평가 질문/expected keyword 추가 보정

## Assumptions

- 최신 기준선은 `eval/results/eval_20260514_152044.json`이다.
- 현 `rag_precision@k_mean=0.60`은 현재 metric 설계상 이론적 상한이다.
- 새 metric은 기존 metric을 대체하지 않고 병행 제공한다.

## Pre-flight checks

- `docs/references/2026-05-14-search-quality-ceiling-analysis.md` 확인
- `eval/pipeline.py`의 기존 metric 계산 방식 확인
- 최신 full eval 리포트 확인

## Steps

1. `normalized_source_precision_at_k()`를 추가한다.
2. `chunk_precision_at_k()`를 추가한다.
3. vector/RAG 경로 모두 새 metric을 계산하도록 report schema를 확장한다.
4. summary에 새 mean 지표를 추가한다.
5. retrieval eval과 full eval을 재실행한다.
6. 결과를 문서화하고 plan을 completed로 이동한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- `.venv/bin/python eval/pipeline.py --metric retrieval`
- `.venv/bin/python eval/pipeline.py --all`

## Manual/Runtime QA

- 새 지표가 기존 리포트 소비자를 깨지 않도록 기존 summary key가 유지되는지 확인한다.
- `source_coverage@k_mean=1.0`과 새 normalized 지표가 해석상 충돌하지 않는지 확인한다.

## Skipped/Not Run

- 검색 튜닝 실험은 metric 정규화 이후로 미룬다.

## Validation Result

- 통과: 문서 검증
  - `bash scripts/validate-docs.sh`
- 통과: Python compile 검증
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- 통과: retrieval eval
  - `.venv/bin/python eval/pipeline.py --metric retrieval`
  - 결과:
    - `normalized_source_precision@k_mean=0.825`
    - `vector_normalized_source_precision@k_mean=0.825`
    - `rag_normalized_source_precision@k_mean=1.0`
    - `vector_chunk_precision@k_mean=0.98`
    - `rag_chunk_precision@k_mean=0.96`
    - `source_recall@k_mean=1.0`
- 통과: full eval
  - `.venv/bin/python eval/pipeline.py --all`
  - 리포트: `eval/results/eval_20260514_164724.json`
  - 결과:
    - `rag_normalized_source_precision@k_mean=1.0`
    - `rag_chunk_precision@k_mean=0.96`
    - `source_recall@k_mean=1.0`
    - `accuracy_mean=0.90`
    - `faithfulness_mean=1.0`
    - `not_found_rate=0.0`

## Open Work

- 없음.

## Completion

- 완료: normalized source precision 지표 추가
- 완료: chunk precision 지표 추가
- 완료: source recall alias 추가
- 완료: 기존 precision 계열 summary key 유지
- 완료: 새 full eval 리포트 생성
  - `eval/results/eval_20260514_164724.json`
- 완료: 결과 문서화
  - `docs/references/2026-05-14-retrieval-metric-normalization.md`
