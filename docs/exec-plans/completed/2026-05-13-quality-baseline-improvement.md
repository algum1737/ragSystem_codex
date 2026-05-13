# Quality Baseline Improvement Plan

## Goal

현재 RAG 평가 기준선(`precision@k_mean=0.48`, `accuracy_mean=0.525`, `faithfulness_mean=0.8`)을 개선하기 위한 다음 실험 범위와 검증 루프를 정한다.

## Scope

- 최신 평가 리포트와 평가 데이터셋 확인
- 검색 실패 케이스 분류
- 청킹, 검색 가중치, reranking, 프롬프트 중 우선 개선 후보 선정
- 다음 실험의 성공 기준 정의

## Assumptions

- 최신 full eval 리포트는 `eval/results/eval_20260513_100727.json`이다.
- 실제 문서 인제스천 상태는 현재 로컬 `chroma_db/` 기준이며, 재현성 확인이 필요하다.
- 구현 변경은 사용자 승인 후 별도 단계에서 진행한다.

## Steps

1. 최신 평가 리포트와 평가 데이터셋 구조를 읽는다.
2. 낮은 점수의 원인을 retrieval, generation, evaluation 기준으로 분류한다.
3. 가장 작은 개선 실험 1개를 제안한다.
4. 성공 기준과 재평가 명령을 문서화한다.

## Risks

- 평가 데이터셋이 작으면 수치 변동이 실제 품질 개선을 충분히 대표하지 못할 수 있다.
- 로컬 Ollama 모델 상태가 바뀌면 generation 지표 비교가 흔들릴 수 있다.

## Validation

- 분석 결과가 `docs/HANDOFF.md` 또는 별도 계획 문서에 남아야 한다.
- 구현 변경 전 개선 실험의 성공 기준이 명확해야 한다.
- 필요 시 `python eval/pipeline.py --all`로 기준선을 재확인한다.

## Open Work

- 없음

## Progress

- 최신 평가 리포트 `eval/results/eval_20260513_100727.json`을 분석했다.
- 평가 데이터셋 `eval/test_cases.json`과 평가 파이프라인 `eval/pipeline.py`를 확인했다.
- 로컬 Chroma DB 기준 chunk/source 분포를 확인했다.
- 분석 결과를 `docs/references/quality-baseline-analysis.md`에 기록했다.

## Findings

- 현재 `precision@k`는 vector-only 검색을 측정한다.
- 실제 답변 생성은 `RAGEngine`에서 vector search, BM25, RRF, Cross-Encoder reranking을 조합한다.
- 따라서 첫 개선 실험은 검색 파라미터 튜닝보다 평가 하네스 정렬이 우선이다.
- `tc-01`, `tc-04`는 문서 근거 부족 또는 질문/데이터셋 불일치 가능성이 높다.
- 여러 케이스는 답변은 맞지만 source 중복과 keyword 문자열 평가 때문에 점수가 낮게 나온다.

## Recommended Next Experiment

- `eval/pipeline.py`에 실제 RAG 검색 경로 기준 retrieval 지표를 추가한다.
- 기존 vector-only precision은 유지하되 `vector_precision@k`로 이름을 분리한다.
- `rag_precision@k`, `source_coverage@k`, `not_found_rate`를 추가한다.

## Verification Notes

- `bash scripts/validate-docs.sh` 통과

## Completion

- 완료일: 2026-05-13
- 최신 기준선의 낮은 점수 원인을 분류했다.
- 첫 개선 실험 후보와 성공 기준을 정했다.
- 남은 작업 없음.
