# Source Drift Watch Case Review Plan

## Goal

source drift 리포트의 watch case를 검토해 평가셋 relevant source를 더 좁힐지, 현 상태를 유지할지 결정한다.

## Scope

- watch case 7건 검토: `tc-02`, `tc-03`, `tc-06`, `tc-07`, `tc-08`, `tc-14`, `tc-15`
- 답변 품질은 유지한 채 source alignment를 개선할 수 있는지 판단
- 필요한 경우 평가셋 보정 후보를 분리

## Out Of Scope

- CI workflow 변경
- 신규 문서 인제스천
- 검색 알고리즘 변경
- 모델 교체

## Assumptions

- 최신 기준선에는 critical source drift가 없다.
- watch case는 생성 지표가 모두 통과하므로 장애가 아니라 source alignment 검토 후보이다.
- 관련 source를 지나치게 좁히면 hard case 일반화가 약해질 수 있다.

## Pre-flight checks

- `docs/references/2026-05-22-source-drift-regression-report.md` 확인
- `eval/results/eval_20260522_160844.json` 확인
- `eval/test_cases.json`의 watch case 확인

## Steps

1. watch case의 missing relevant source와 unexpected RAG source를 분류한다.
2. 평가셋 relevant source가 과도하게 넓은지 확인한다.
3. 검색 결과가 실제로 틀린 문서를 끌어오는지, 확장 corpus의 동등 근거를 끌어오는지 판단한다.
4. 보정 필요 여부를 문서화한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- source drift report와 최신 eval 결과를 대조한다.

## Skipped/Not Run

- 아직 실행 전.

## Validation Result

- 아직 실행 전.

## Open Work

- watch case 검토 진행.
