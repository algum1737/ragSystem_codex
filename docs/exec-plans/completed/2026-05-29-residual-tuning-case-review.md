# Residual Tuning Case Review Plan

## Goal

성능 안정화 기준 통과 이후 남은 `tc-04` faithfulness 실패와 `tc-17` source recall 저하를 검토해 추가 튜닝 필요 여부를 결정한다.

## Scope

- `eval/results/eval_20260529_173928.json`의 잔여 케이스 분석
- `tc-04` faithfulness 실패 원인 분류
- `tc-17` relevant source 범위와 검색 결과 비교
- 추가 튜닝이 필요한지, 문서화된 예외로 둘지 결정

## Out Of Scope

- 운영 모델 변경
- 대규모 검색 파라미터 변경
- 평가셋 전체 재설계

## Assumptions

- 현재 안정화 기준은 통과했다.
- 추가 튜닝은 잔여 케이스 분석 후 필요성이 확인될 때만 수행한다.

## Pre-flight checks

- `git status --short --branch` 확인
- 최신 리포트 `eval/results/eval_20260529_173928.json` 존재 확인
- 관련 평가 케이스와 retrieved source 확인

## Steps

1. `tc-04` 답변, context, faithfulness judge 입력을 확인한다.
2. `tc-17`의 relevant source와 RAG retrieved source를 비교한다.
3. 추가 구현, 평가셋 보정, 문서화 예외 중 하나로 결정한다.
4. 결정 내용을 참조 문서와 handoff에 기록한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- 필요 시 `.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5`

## Manual/Runtime QA

- 잔여 케이스의 답변과 검색 source를 사람이 검토한다.

## Skipped/Not Run

- 채택하지 않은 전역 프롬프트 실험 리포트 `eval/results/eval_20260601_085420.json`은 기준 리포트로 커밋하지 않았다.

## Completion

- `eval/results/eval_20260529_173928.json` 기준 `tc-04`, `tc-17` 잔여 케이스를 분석했다.
- `tc-04`는 검색 누락이 아니라 답변 citation 표현 또는 faithfulness judge 안정성 문제로 분류했다.
- 전역 출처 번호 프롬프트 보강을 서버에서 실험했지만 full eval에서 `tc-05`, `tc-07`, `tc-11` 회귀가 발생해 채택하지 않았다.
- `tc-17`은 답변 품질이 아니라 relevant source scope가 넓은 평가셋 문제 후보로 분류했다.
- 결과 문서 `docs/references/2026-06-01-residual-tuning-case-review.md`를 추가했다.
- 다음 active plan `docs/exec-plans/active/2026-06-01-tc04-faithfulness-tc17-source-scope.md`를 생성했다.

## Validation Result

- 통과: `git status --short --branch`
- 통과: `eval/results/eval_20260529_173928.json`의 `tc-04`, `tc-17` 분석
- 실패/미채택: 전역 출처 번호 프롬프트 실험 full eval
  - `accuracy_mean=0.9783`, `faithfulness_mean=0.9565`, `not_found_success_rate=1.0`
  - source drift guard critical: `tc-05`, `tc-07`, `tc-11`
- 통과: 서버 배포본은 채택하지 않은 프롬프트 변경을 원복했다.

## Open Work

- 없음.
