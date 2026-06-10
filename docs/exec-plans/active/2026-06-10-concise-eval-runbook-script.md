# Concise Eval Runbook Script Plan

## Goal

서버 concise lightweight eval smoke를 반복 가능하게 실행할 수 있도록 runbook 또는 script를 정리한다.

## Scope

- 서버 smoke 명령의 표준 trace/report naming 정리
- 필요 시 로컬 script 추가
- 수동 배포 후 실행 절차 문서화
- 실패 시 확인할 summary/trace 기준 정리

## Out Of Scope

- GitHub Actions에서 Ollama 기반 runtime eval 실행
- 운영 기본 answer mode 변경
- 프롬프트 변경
- full eval 기본 gate 변경

## Assumptions

- concise runtime eval은 서버에서만 안정적으로 실행 가능하다.
- CI에는 schema 검증만 유지한다.
- 서버 경로는 `/opt/ragSystem_codex`다.

## Pre-flight checks

- `git status --short --branch`
- `docs/references/2026-06-10-concise-eval-ci-promotion-result.md` 확인
- 서버 smoke 결과 문서 확인

## Steps

1. 서버 smoke에 필요한 명령과 환경변수를 정리한다.
2. script로 승격할지 runbook 문서로 둘지 결정한다.
3. 선택한 방식으로 반복 실행 절차를 추가한다.
4. 문서 검증과 필요한 정적 검증을 실행한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- 필요 시 추가 script syntax check

## Manual/Runtime QA

- 필요 시 서버 smoke 명령을 재확인한다.

## Skipped/Not Run

- full eval은 실행하지 않는다.

## Open Work

- runbook 또는 script 방식 결정
- 반복 실행 절차 추가
