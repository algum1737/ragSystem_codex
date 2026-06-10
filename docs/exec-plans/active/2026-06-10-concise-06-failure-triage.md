# Concise 06 Failure Triage Plan

## Goal

runbook script가 감지한 `concise-06` 실패를 분석해 prompt 문제인지 평가 기준 문제인지 결정한다.

## Scope

- `concise-06` 최근 실패 report와 trace 확인
- 답변 누락 항목과 retrieved source를 비교
- required point 기준이 과한지, concise prompt가 통지 수단/예외를 누락하는지 판단
- 후속 조치 후보 정리

## Out Of Scope

- 프롬프트 즉시 변경
- 운영 기본 answer mode 변경
- full eval 실행
- 자동 라우팅 구현

## Assumptions

- `concise-06`은 유료서비스 중단/변경 통지 케이스다.
- 최근 실패 report는 서버 `/opt/ragSystem_codex/eval/results/concise_eval_20260610_114205.json`이다.
- failure detection script 자체는 정상 동작했다.

## Pre-flight checks

- `git status --short --branch`
- `docs/references/2026-06-10-concise-eval-runbook-script-result.md` 확인
- 서버 failure report 또는 로컬 기록 확인

## Steps

1. `concise-06` 실패 답변과 required point mismatch를 재검토한다.
2. retrieved source에 통지 수단/예외가 충분히 포함됐는지 확인한다.
3. 평가 기준 조정, prompt 보강, 또는 현 상태 유지 중 하나를 결정한다.
4. 필요하면 별도 구현 계획을 만든다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 필요 시 서버 `concise-06` 단일 query 또는 runbook script 재실행

## Skipped/Not Run

- full eval은 실행하지 않는다.

## Open Work

- `concise-06` 실패 원인 분류
- 후속 조치 결정
