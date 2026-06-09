# Push And CI Verification Plan

## Goal

로컬 `main`에 누적된 커밋을 원격에 push하고 GitHub Actions 상태를 확인한다.

## Scope

- 로컬 브랜치 ahead 상태 확인
- push 실행
- GitHub Actions 실행 상태 확인
- 실패 시 원인 분류
- handoff 갱신

## Out Of Scope

- 추가 기능 구현
- PR 생성
- 브랜치 전략 변경
- CI 설정 변경

## Assumptions

- GitHub Actions는 다시 사용 가능하도록 복구된 상태다.
- 현재 작업은 `main`에서 진행 중이다.
- 원격 반영 시 `main` push workflow가 실행될 수 있다.

## Pre-flight checks

- `git status --short --branch`
- `git log --oneline origin/main..HEAD`
- 로컬 검증 결과 확인

## Steps

1. push 전 브랜치와 ahead 커밋을 확인한다.
2. `git push`를 실행한다.
3. GitHub Actions run 상태를 확인한다.
4. 결과를 handoff에 기록한다.

## Automated tests

- push 전 로컬 검증은 이전 follow-up plan에서 통과했다.
- 필요 시 `gh run list` 또는 `gh run watch`로 CI 상태를 확인한다.

## Manual/Runtime QA

- GitHub Actions UI 또는 `gh` 결과에서 run 상태를 확인한다.

## Skipped/Not Run

- 추가 full eval은 실행하지 않는다.

## Open Work

- push
- CI 확인
