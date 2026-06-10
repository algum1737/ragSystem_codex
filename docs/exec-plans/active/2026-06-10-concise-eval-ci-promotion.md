# Concise Eval CI Promotion Plan

## Goal

concise lightweight eval을 CI 또는 배포 후 수동 검증 루프에 승격할지 결정한다.

## Scope

- 현재 GitHub Actions 환경에서 실행 가능한 검증과 서버 전용 검증을 분리
- `--concise-lightweight`를 CI에 넣을지, 서버 smoke 절차로만 둘지 판단
- 필요 시 문서 또는 스크립트 후보 정의

## Out Of Scope

- 프롬프트 변경
- 운영 기본 answer mode 변경
- 자동 라우팅 구현
- full eval 기본 gate 변경

## Assumptions

- concise lightweight eval은 Ollama와 Chroma corpus가 필요하다.
- GitHub Actions CI에는 운영 corpus와 Ollama가 없다.
- 서버 smoke는 운영 환경에서는 실행 가능하다.

## Pre-flight checks

- `git status --short --branch`
- 최신 server verification result 확인
- GitHub Actions 현재 workflow 확인

## Steps

1. 현재 CI workflow가 실행할 수 있는 검증 범위를 확인한다.
2. concise lightweight eval을 CI에 직접 넣을 때의 비용과 불가능 조건을 정리한다.
3. 배포 후 수동 검증 또는 서버 스크립트로 둘 때의 절차를 정리한다.
4. 승격 여부와 후속 구현 필요성을 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 필요 시 서버 concise lightweight eval 명령을 dry-run 형태로 재확인한다.

## Skipped/Not Run

- full eval은 실행하지 않는다.
- CI workflow 변경은 판단 후 별도 승인으로 진행한다.

## Open Work

- CI 승격 여부 결정
- 서버 수동 검증 절차 문서화 또는 스크립트화 필요성 결정
