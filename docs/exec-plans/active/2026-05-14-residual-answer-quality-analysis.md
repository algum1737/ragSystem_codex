# Residual Answer Quality Analysis Plan

## Goal

검색 지표 정규화 이후 남은 답변 accuracy 병목을 분석하고, 다음 답변 품질 개선 후보를 하나로 좁힌다.

## Scope

- 최신 리포트 `eval/results/eval_20260514_164724.json` 기준 낮은 `answer_accuracy` 케이스 분석
- `tc-06`, `tc-07`, `tc-09`의 답변, expected keyword, 문서 근거 대조
- expected keyword 정합성 문제와 프롬프트/답변 형식 문제를 분리

## Out Of Scope

- 즉시 구현 변경
- 검색 튜닝
- Ollama 모델 교체
- 외부 API 평가 도입

## Assumptions

- 최신 RAG 검색 경로는 source 기준 병목이 아니다.
- 최신 검색 지표는 `rag_normalized_source_precision@k_mean=1.0`, `source_recall@k_mean=1.0`이다.
- 남은 품질 병목은 답변 표현 또는 expected keyword 정합성일 가능성이 높다.

## Pre-flight checks

- 최신 full eval 리포트 확인
- `eval/test_cases.json`의 `tc-06`, `tc-07`, `tc-09` expected keyword 확인
- 해당 케이스 답변과 retrieved context 확인

## Steps

1. 낮은 `answer_accuracy` 케이스를 추출한다.
2. 답변이 문서 근거에는 충실한지 확인한다.
3. expected keyword 불일치와 답변 누락을 분리한다.
4. 다음 구현 후보를 평가셋 보정, 프롬프트 보정, 또는 no-op으로 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`

## Manual/Runtime QA

- `tc-06`, `tc-07`, `tc-09` 답변을 직접 읽고 expected keyword와 대조한다.

## Skipped/Not Run

- 구현 전 분석 계획이므로 full eval 재실행은 기본 검증에서 제외한다.

## Validation Result

- 아직 실행 전.

## Open Work

- 잔여 낮은 answer accuracy 케이스 분석
- 다음 답변 품질 개선 후보 선정
