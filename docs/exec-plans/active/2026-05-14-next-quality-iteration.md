# Next Quality Iteration Plan

## Goal

검색 품질 1차 개선 이후 다음 품질 병목을 재분류하고, 다음 실험 후보를 하나로 좁힌다.

## Scope

- 최신 리포트 `eval/results/eval_20260514_113849.json` 분석
- 남은 낮은 점수 케이스 확인
- 청킹, hybrid search 가중치, reranking 적용 범위, 평가셋 확장 후보 비교
- 다음 구현 실험 계획 수립

## Out Of Scope

- 즉시 구현 변경
- Ollama 모델 교체
- 외부 API 평가 도입

## Assumptions

- 최신 기준선은 `eval/results/eval_20260514_113849.json`이다.
- 검색 지표는 1차 목표에 도달했으므로 다음 병목은 케이스별 답변 품질 또는 평가셋 정합성일 수 있다.

## Pre-flight checks

- `main`과 `origin/main` 동기화 확인
- active/completed 계획 정합성 확인
- 최신 full eval 리포트 확인

## Steps

1. 최신 full eval 리포트를 케이스별로 분석한다.
2. 낮은 accuracy/faithfulness/not_found 케이스를 재분류한다.
3. 다음 개선 후보를 비용과 리스크 기준으로 비교한다.
4. 사용자 승인 후 구현 계획을 별도 active plan으로 승격한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`

## Manual/Runtime QA

- 최신 리포트의 낮은 점수 케이스 답변과 검색 source를 직접 확인한다.

## Skipped/Not Run

- 구현 전이므로 full eval 재실행은 이 계획의 기본 검증에서 제외한다.

## Validation Result

- 통과: 최신 리포트 `eval/results/eval_20260514_113849.json` 확인
- 통과: 작업 리포트 작성
  - `docs/references/2026-05-14-work-report.md`
- 통과: before/after 비교 문서 작성
  - `docs/references/2026-05-14-before-after.md`
- 통과: 기존 RAG 요약 문서 최신화
  - `RAG_IMPROVEMENT_ROADMAP.md`
  - `RAG_BEFORE_AFTER.md`
  - `RAG_PERFORMANCE_REPORT.md`

## Open Work

- 최신 리포트 분석
- 다음 실험 후보 선정
