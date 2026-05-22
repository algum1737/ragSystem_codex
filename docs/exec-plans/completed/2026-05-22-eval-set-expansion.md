# Eval Set Expansion Plan

## Goal

최신 13개 문서, 318개 청크 corpus를 더 잘 검증하도록 평가셋을 확장한다.

## Scope

- `eval/test_cases.json`에 hard case 추가
- 유료서비스, 운영정책, 위치기반서비스, negative/partial-answer 케이스 보강
- 확장 후 full eval 결과를 기존 10개 케이스 기준선과 비교

## Out Of Scope

- 검색 알고리즘 튜닝
- 프롬프트 변경
- 모델 교체
- DB 초기화 및 재인제스천

## Assumptions

- 현재 corpus는 `/stats count=318` 기준이다.
- 현재 평가셋 10개 케이스는 기존 다음/네이버 일반·위치기반 약관 중심이다.
- 평가셋 확장 전 검토 결과는 `docs/references/2026-05-22-eval-generalization-review.md`를 기준으로 한다.

## Pre-flight checks

- 최신 active/completed plan 상태 확인
- `eval/test_cases.json` 현재 구조 확인
- 신규 hard case의 source 파일명이 실제 인제스천 source와 일치하는지 확인

## Steps

1. hard case 후보 중 우선 6개를 `eval/test_cases.json`에 추가한다.
2. 각 케이스에 `expected_keywords`, `relevant_sources`, `doc_type`을 명시한다.
3. docs/reference에 확장 의도와 기대 검증 영역을 기록한다.
4. full eval을 재실행하고 기존 10개 및 신규 케이스 점수를 분리해 해석한다.
5. 실패 케이스를 검색 실패, 답변 실패, 평가 기준 실패로 분류한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- `.venv/bin/python eval/pipeline.py --all`

## Manual/Runtime QA

- 신규 케이스 질문이 실제 문서 근거와 맞는지 확인한다.
- keyword OR group이 지나치게 넓지 않은지 확인한다.
- full eval 결과에서 기존 10개 케이스 회귀 여부를 확인한다.

## Skipped/Not Run

- `eval/results/eval_20260522_090505.json`은 sandbox 경로에서 Ollama 연결 실패로 생성 지표가 비어 있어 최종 결과로 사용하지 않는다.

## Validation Result

- Pre-flight checks
  - active/completed plan 상태 확인 완료.
  - `eval/test_cases.json` 현재 구조 확인 완료.
  - hard case source가 최신 인제스천 source와 맞는지 확인하고 케이스를 추가.
- Automated tests
  - `bash scripts/validate-docs.sh` 통과.
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py` 통과.
  - `.venv/bin/python eval/pipeline.py --all` 실행 완료.
    - 최종 리포트: `eval/results/eval_20260522_091248.json`
    - `accuracy_mean=0.9062`
    - `faithfulness_mean=0.75`
    - `not_found_rate=0.0625`
    - `rag_normalized_source_precision@k_mean=0.7188`
    - `rag_chunk_precision@k_mean=0.5`
- Manual/Runtime QA
  - 신규 케이스 `tc-11`~`tc-16` 추가.
  - 기존 10개와 신규 6개 결과를 분리해 해석.
  - 실패 케이스를 `docs/references/2026-05-22-eval-set-expansion-result.md`에 기록.

## Open Work

- 남은 작업 없음.
- 다음 후보: negative case 채점 정책 및 faithfulness context selection 재검토.
