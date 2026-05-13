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

- 최신 평가 리포트 분석
- 실패 케이스 분류
- 첫 개선 실험 후보 선정
