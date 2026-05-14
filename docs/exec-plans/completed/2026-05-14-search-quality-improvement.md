# Search Quality Improvement Plan

## Goal

현재 검색 기준선 `precision@k_mean=0.48`, `rag_precision@k_mean=0.54`를 분석하고, 실제 RAG 검색 경로의 1차 개선 목표인 `rag_precision@k_mean=0.60+`에 도달하기 위한 최소 변경안을 검증한다.

## Scope

- 최신 평가 리포트와 실패 케이스 분석
- 청킹, hybrid search 가중치, reranking 적용 범위, 카테고리 필터링 후보 점검
- 검색 품질 개선을 위한 작은 구현 실험
- 전체 eval 재실행과 기준선 비교

## Out Of Scope

- Ollama 모델 교체
- 외부 API 기반 평가 도입
- UI/API 기능 확장
- PPTX 생성 품질 개선

## Assumptions

- 현재 Chroma 데이터와 로컬 모델 캐시는 유지되어 있다.
- 최신 기준선은 `eval/results/eval_20260513_164755.json`과 관련 문서 분석을 기준으로 한다.
- 검색 품질 개선은 답변 생성 프롬프트 변경보다 먼저 수행한다.

## Pre-flight checks

- 현재 브랜치와 PR 상태 확인
- 최신 eval 리포트와 `docs/references/quality-baseline-analysis.md` 확인
- 검색 경로 코드 위치 확인: `retriever/engine.py`, `eval/pipeline.py`, ingestion 청킹 코드
- 로컬 런타임 의존성 확인: Chroma 데이터, 임베딩 모델 캐시, Cross-Encoder 캐시, Ollama 상태

## Steps

1. 최신 평가 결과에서 낮은 검색 점수 케이스를 재분류한다.
2. 검색 실패 원인을 청킹, 후보 검색, 재랭킹, 필터링, 평가셋 문제로 나눈다.
3. 가장 작은 개선 후보 1개를 선택해 구현한다.
4. retrieval eval과 full eval을 실행해 기준선과 비교한다.
5. 개선 효과와 부작용을 계획 문서와 참조 문서에 기록한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- `.venv/bin/python eval/pipeline.py --metric retrieval`
- `.venv/bin/python eval/pipeline.py --all`

## Manual/Runtime QA

- 낮은 점수 테스트 케이스의 검색 결과와 근거 청크를 직접 확인한다.
- 개선 전후 주요 지표를 비교한다.

## Skipped/Not Run

- GitHub Actions full eval: Ollama, Chroma 데이터, 로컬 모델 캐시 의존성 때문에 CI 범위에서 제외한다.
- 외부 API 평가: 완전 로컬 실행 제약 때문에 제외한다.

## Validation Result

- 통과: `bash scripts/validate-docs.sh`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- 통과: `.venv/bin/python eval/pipeline.py --metric retrieval`
  - `vector_precision@k_mean=0.48`
  - `rag_precision@k_mean=0.60`
  - `source_coverage@k_mean=1.0`
- 통과: `.venv/bin/python eval/pipeline.py --all`
  - 리포트: `eval/results/eval_20260514_113849.json`
  - 검색 지표는 저장됨: `rag_precision@k_mean=0.60`, `source_coverage@k_mean=1.0`
  - 생성 지표도 산출됨: `accuracy_mean=0.70`, `faithfulness_mean=0.90`, `not_found_rate=0.10`
- 통과: PR #16 GitHub Actions `Static checks`
  - 6초 만에 통과했다.

## Open Work

- 없음

## Completion

- PR #16을 머지했다.
- 로컬 `main`을 `origin/main`과 동기화했다.
- 검색 품질 1차 목표를 달성했다.
  - `rag_precision@k_mean`: `0.54 -> 0.60`
  - `source_coverage@k_mean`: `0.925 -> 1.0`
- Ollama 기동 상태에서 full eval 생성 지표까지 재확인했다.
