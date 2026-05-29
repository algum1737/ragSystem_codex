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

- `eval/test_cases.json` 보정은 실행하지 않는다.
  - 이유: source scope 정책 결정이 목표이며, watch case를 현재 retrieval 결과에 맞춰 즉시 확장하면 평가셋 과적합 위험이 있다.
- full eval 재실행은 실행하지 않는다.
  - 이유: 평가셋과 검색/생성 코드 변경이 없고, 최신 full eval의 생성 지표가 이미 모두 통과 상태다.

## Validation Result

- Pre-flight checks
  - `docs/references/2026-05-22-watch-case-review.md` 확인.
  - `docs/references/2026-05-22-source-drift-regression-report.md` 확인.
  - `eval/test_cases.json`의 watch case source 범위 확인.
- Automated tests
  - `bash scripts/validate-docs.sh` 통과.
- Manual/Runtime QA
  - watch case review와 source drift report를 대조했다.
  - watch case 7건은 생성 지표 실패가 아니라 대표 근거 범위와 확장 corpus의 동등 근거 사이의 정책 문제로 판단했다.
  - 정책 결과 문서: `docs/references/2026-05-28-source-scope-policy.md`

## Open Work

- 남은 작업 없음.
- 다음 후보: source scope policy에 따라 `tc-02`, `tc-03`, `tc-07`, `tc-08`, `tc-14`, `tc-15`를 별도 active plan에서 케이스 분리 후보로 검토한다.
