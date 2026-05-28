# Source Scope Policy Plan

## Goal

평가셋의 `relevant_sources` 범위를 어떻게 정의할지 기준을 정한다.

## Scope

- 일반약관, 위치기반서비스, 유료서비스, 운영정책이 동시에 걸리는 질문의 source 범위 기준 검토
- source recall을 가능한 모든 관련 문서 기준으로 볼지, 답변에 충분한 대표 근거 기준으로 볼지 결정
- watch case 보정 전 적용할 정책 문서화

## Out Of Scope

- 신규 문서 인제스천
- 검색 알고리즘 변경
- 모델 교체
- 즉시 full eval 재실행

## Assumptions

- watch case는 생성 지표 실패가 아니라 source scope 정책 부재에서 비롯된 후보이다.
- `relevant_sources`를 현재 retrieved source에 맞춰 단순 확장하면 과적합 위험이 있다.
- source scope 기준을 먼저 정한 뒤 평가셋 보정 여부를 판단해야 한다.

## Pre-flight checks

- `docs/references/2026-05-22-watch-case-review.md` 확인
- `docs/references/2026-05-22-source-drift-regression-report.md` 확인
- `eval/test_cases.json`의 watch case source 범위 확인

## Steps

1. source scope를 "전체 관련 문서" 기준으로 둘 때의 장단점을 정리한다.
2. source scope를 "대표 근거 문서" 기준으로 둘 때의 장단점을 정리한다.
3. 평가 목적별 source scope 정책을 선택한다.
4. 정책에 따라 watch case 보정 필요 여부를 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- watch case review 결과와 source drift report를 대조한다.

## Skipped/Not Run

- 아직 실행 전.

## Validation Result

- 아직 실행 전.

## Open Work

- source scope policy 검토 진행.
