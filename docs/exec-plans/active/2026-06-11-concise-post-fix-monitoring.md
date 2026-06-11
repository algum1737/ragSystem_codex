# Concise Post-Fix Monitoring Plan

## Goal

`concise-06` 안정화 변경 이후 운영 trace와 짧은 smoke를 확인해 concise prompt 보강이 실제 운영 질문에서 불필요한 bullet을 줄이고 필수 예외를 유지하는지 점검한다.

## Scope

- 운영 API/Web health 확인
- 최근 `api.query` trace에서 `answer_mode=concise` 표본 확인
- 필요 시 `concise-06` 운영 API smoke 1회 재확인
- 후속 경량 케이스 확장 필요 여부 결정

## Out Of Scope

- prompt 추가 변경
- eval case 추가
- full eval 실행
- 운영 기본 answer mode 변경

## Assumptions

- 현재 `CONCISE_PROMPT_TEMPLATE`는 서버 운영 API에 반영되어 있다.
- 서버 trace는 privacy-safe metadata 중심으로 기록된다.
- 실제 사용자 질의 표본이 부족하면 수동 smoke 중심으로 판단한다.

## Pre-flight checks

- `git status --short --branch`
- 서버 `/health`
- Streamlit `_stcore/health`

## Steps

1. 운영 API/Web health를 확인한다.
2. 최근 trace에서 `answer_mode=concise` 표본 수와 latency/answer length를 확인한다.
3. 표본이 부족하면 `concise-06` API smoke를 1회 실행한다.
4. 불필요한 bullet 재발 또는 예외 누락 여부를 기록한다.
5. 추가 경량 케이스 확장이 필요한지 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 health 확인
- 최근 trace 또는 API smoke 확인

## Skipped/Not Run

- full eval은 실행하지 않는다. post-fix 운영 모니터링 범위다.

## Open Work

- 운영 trace 표본 확인
