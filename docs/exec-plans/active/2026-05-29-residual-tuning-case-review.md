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

- 아직 잔여 케이스 리뷰는 수행하지 않았다.

## Open Work

- `tc-04`, `tc-17` 잔여 케이스 리뷰.
