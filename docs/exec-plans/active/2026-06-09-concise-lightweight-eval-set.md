# Concise Lightweight Eval Set Plan

## Goal

선택형 `concise` answer mode가 짧은 답변을 만들면서 필수 근거와 예외사항을 누락하지 않는지 확인할 수 있는 경량 평가셋과 판정 기준을 정의한다.

## Scope

- concise mode 전용 대표 질의 후보 선정
- 필수 keyword 또는 required point 기준 정의
- no-answer/문서 미확인 케이스 포함 여부 결정
- trace 기반 latency/source count 확인 기준 정리

## Out Of Scope

- 운영 기본 answer mode 변경
- 자동 라우팅 구현
- full eval 재실행
- 프롬프트 변경

## Assumptions

- `concise`는 선택형 모드로 유지한다.
- 현재 trace 표본은 방향성 판단에는 충분하지만 품질 보증에는 부족하다.
- 경량 평가셋은 full eval을 대체하지 않고 concise mode 회귀 감지용으로만 사용한다.

## Pre-flight checks

- `git status --short --branch`
- 관련 결과 문서 확인: `docs/references/2026-06-09-concise-mode-trace-review.md`
- active plan 존재 확인

## Steps

1. 기존 eval case와 최근 trace 질문 유형에서 concise 후보를 고른다.
2. 각 case의 필수 포함 사항과 불필요한 확정 표현 금지 기준을 정한다.
3. 경량 평가셋을 문서로 먼저 고정한다.
4. 구현이 필요하면 별도 승인 후 eval harness 반영 계획으로 분리한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 필요 시 운영 `/query` `answer_mode=concise` 대표 질의 1~2건 확인

## Skipped/Not Run

- 이 계획 자체에서는 full eval을 실행하지 않는다.
- eval harness 코드 변경은 사용자 승인 후 별도 작업으로 진행한다.

## Open Work

- concise mode 경량 평가셋 후보 정의
- 구현 필요 여부 결정
