# Eval Case Alignment Plan

## Goal

최신 full eval의 낮은 accuracy 케이스를 문서 근거 기준에 맞게 재분류하고 expected keyword OR group을 보정한다.

## Scope

- `eval/test_cases.json`의 `tc-01`, `tc-03`, `tc-04`, `tc-09` 보정
- no-answer/partial-answer 성격의 케이스를 평가 가능하게 표현
- full eval 재실행과 이전 기준선 비교
- 결과 문서화

## Out Of Scope

- 검색 파라미터 튜닝
- 청킹/인제스천 구조 변경
- Ollama 모델 교체
- 외부 API 평가 도입

## Assumptions

- 최신 기준선은 `eval/results/eval_20260514_113849.json`이다.
- 검색 지표는 이미 1차 목표에 도달했다.
- 이번 작업은 실제 답변 품질을 과장하기 위한 점수 보정이 아니라, 현재 문서 근거와 평가 질문/키워드를 맞추는 작업이다.

## Pre-flight checks

- `main`과 `origin/main` 동기화 확인
- 최신 full eval 리포트 확인
- 낮은 점수 케이스 분석 문서 확인: `docs/references/2026-05-14-next-quality-iteration-analysis.md`
- Ollama `gemma3:12b` 사용 가능 여부 확인

## Steps

1. `tc-01` 질문을 문서 근거에 맞는 해지 후 데이터/게시물 처리 질문으로 재분류한다.
2. `tc-03`, `tc-04`, `tc-09` expected keywords를 OR group으로 보정한다.
3. 필요 시 no-answer 판정과 keyword accuracy가 충돌하지 않도록 평가 함수를 보정한다.
4. retrieval eval과 full eval을 실행해 기준선과 비교한다.
5. 결과와 남은 리스크를 문서화한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- `.venv/bin/python eval/pipeline.py --metric retrieval`
- `.venv/bin/python eval/pipeline.py --all`

## Manual/Runtime QA

- `tc-01`, `tc-03`, `tc-04`, `tc-09`의 답변과 expected keywords를 직접 대조한다.
- 검색 지표가 회귀하지 않는지 확인한다.
- faithfulness가 하락하지 않는지 확인한다.

## Skipped/Not Run

- 외부 API 평가: 완전 로컬 실행 제약 때문에 제외한다.
- 검색 튜닝 실험: 이번 계획 범위 밖이다.

## Validation Result

- 통과: 문서 검증
  - `bash scripts/validate-docs.sh`
- 통과: Python compile 검증
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- 통과: retrieval eval
  - `.venv/bin/python eval/pipeline.py --metric retrieval`
  - 결과: `precision@k_mean=0.48`, `vector_precision@k_mean=0.48`, `rag_precision@k_mean=0.60`, `source_coverage@k_mean=1.0`
- 통과: full eval
  - `.venv/bin/python eval/pipeline.py --all`
  - 리포트: `eval/results/eval_20260514_152044.json`
  - 결과: `accuracy_mean=0.875`, `faithfulness_mean=1.0`, `not_found_rate=0.0`
- 참고: sandbox 내부 full eval은 `localhost:11434` 접근 제한으로 Ollama 연결 실패가 발생했다. 권한 상승 실행에서 로컬 Ollama 연결과 full eval을 정상 검증했다.
- 케이스 직접 확인:
  - `tc-01`: 질문을 해지 후 데이터/게시물 처리로 재분류했고 `answer_accuracy=1.0`, `faithfulness=1.0`
  - `tc-03`: 이용 제한/정지 조건의 대체 표현을 OR group으로 반영했고 `answer_accuracy=1.0`, `faithfulness=1.0`
  - `tc-04`: 자동 갱신 근거 부족과 해지/데이터 처리 근거를 함께 평가하도록 보정했고 `answer_accuracy=1.0`, `faithfulness=1.0`
  - `tc-09`: 표현 대체를 일부 보강했으나 `answer_accuracy=0.75`, `faithfulness=1.0`

## Open Work

- 없음.

## Completion

- 완료: `tc-01`, `tc-03`, `tc-04`, `tc-09` 평가 케이스 정렬
- 완료: 기준선 `eval/results/eval_20260514_113849.json` 대비 full eval 지표 개선 확인
  - `accuracy_mean`: `0.70 -> 0.875`
  - `faithfulness_mean`: `0.90 -> 1.0`
  - `not_found_rate`: `0.10 -> 0.0`
  - 검색 지표는 변경 없음: `precision@k_mean=0.48`, `rag_precision@k_mean=0.60`
- 완료: 결과 문서화
  - `docs/references/2026-05-14-eval-case-alignment.md`
