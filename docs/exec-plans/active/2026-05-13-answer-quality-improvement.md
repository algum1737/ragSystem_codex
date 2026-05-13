# Answer Quality Improvement Plan

## Goal

새 평가 하네스 기준으로 검색보다 답변 품질과 평가셋 정합성 문제를 우선 개선한다.

## Scope

- 최신 리포트 `eval/results/eval_20260513_134658.json` 분석
- `accuracy_mean`이 낮은 케이스 분류
- `not_found_rate` 발생 케이스의 문서 근거 여부 확인
- 프롬프트 개선, 평가 키워드 보정, 테스트 케이스 정리 중 첫 구현 후보 선정

## Assumptions

- `source_coverage@k_mean=0.925`이므로 우선 병목은 검색 누락보다 답변/평가 정합성일 가능성이 높다.
- `accuracy_mean`은 키워드 기반 단순 지표이므로 실제 답변 품질과 불일치할 수 있다.
- 구현 변경은 사용자 승인 후 진행한다.

## Steps

1. `accuracy_mean`이 낮은 케이스를 리포트에서 추출한다.
2. 낮은 원인을 문서 근거 부족, 프롬프트 문제, 평가 키워드 문제로 분류한다.
3. 가장 작은 구현 실험 1개를 정한다.
4. 성공 기준과 재평가 명령을 문서화한다.

## Risks

- LLM 응답은 실행마다 약간 달라져 accuracy 수치가 흔들릴 수 있다.
- 평가 키워드를 과도하게 맞추면 실제 답변 품질보다 테스트 통과에 치우칠 수 있다.

## Validation

- 분석 결과가 문서화되어야 한다.
- 첫 구현 실험의 성공 기준이 명확해야 한다.
- 필요 시 `.venv/bin/python eval/pipeline.py --all`로 기준선을 재확인한다.

## Open Work

- 낮은 accuracy 케이스 분석
- `not_found` 케이스 문서 근거 확인
- 첫 구현 실험 후보 선정
