# Agent Loop Harness Migration

## Goal

Codex agent loop 관점을 기존 `ragSystem_codex` 하네스에 병합해, RAG/eval 작업의 시작 맥락, 계획, 도구 관찰, 검증, 인계 흐름을 문서와 검증 스크립트에서 명확히 한다.

## Scope

- `docs/AGENT_LOOP.md` 추가
- `AGENTS.md`, `docs/index.md`, `docs/PLANS.md`, `docs/HANDOFF.md`에 agent loop 문서와 운영 관계 연결
- `scripts/validate-docs.sh`에 agent loop 문서와 active plan 관찰/검증 섹션 검사 추가
- 기존 active plan 2개에 `Observation Log`와 `Validation Result` 섹션 추가
- 마이그레이션 완료 범위와 검증 결과 기록 후 completed plan으로 이동

## Out Of Scope

- 제품 코드 변경
- RAG prompt, retrieval, eval rule 변경
- full eval 또는 서버 runtime QA
- 기존 active plan의 작업 상태 변경

## Assumptions

- 현재 변경은 하네스 문서와 검증 스크립트 보강만 다룬다.
- 기존 active plan 2개는 완료하지 않고, 새 검증 계약에 맞는 섹션만 추가한다.
- `docs/HANDOFF.md`는 필요한 시작 맥락과 최근 진행 요약만 최소 수정한다.

## Pre-flight checks

- 현재 작업 브랜치: `docs/agent-loop-harness-migration`
- 마이그레이션 전 `bash scripts/validate-docs.sh` 통과 확인
- 마이그레이션 전 `docs/AGENT_LOOP.md`는 존재하지 않음
- 기존 active plan:
  - `docs/exec-plans/active/2026-06-11-concise-real-usage-trace-review.md`
  - `docs/exec-plans/active/2026-06-24-hard-eval-second-expansion-failure-triage.md`

## Steps

1. `docs/AGENT_LOOP.md`를 추가한다.
2. `AGENTS.md`의 First Reads와 Key Docs에 agent loop 문서를 추가한다.
3. `docs/index.md`의 Core Documents에 agent loop 문서를 추가한다.
4. `docs/PLANS.md`에 `/goal`, `/plan`, exec plan, HANDOFF 관계와 `Observation Log` 기준을 추가한다.
5. `docs/HANDOFF.md`의 Read First와 최근 진행 상태에 agent loop 마이그레이션을 반영한다.
6. 기존 active plan 2개에 `Observation Log`와 `Validation Result` 섹션을 추가한다.
7. `scripts/validate-docs.sh`에 `docs/AGENT_LOOP.md`, `Observation Log`, `Validation Result` 검사를 추가한다.
8. 검증 후 이 계획을 completed로 이동하고 `docs/index.md`, `docs/HANDOFF.md`를 갱신한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `rg '<[A-Z_]+>' . --glob '!*.pyc' --glob '!__pycache__/**' --glob '!.venv/**' --glob '!chroma_db/**'`

## Manual/Runtime QA

- `AGENTS.md`, `docs/index.md`, `docs/PLANS.md`, `docs/HANDOFF.md`가 `docs/AGENT_LOOP.md`를 과도한 중복 없이 가리키는지 확인한다.
- 기존 active plan 2개가 완료 처리되지 않고 open work 상태를 유지하는지 확인한다.

## Skipped/Not Run

- 제품 코드 테스트, full eval, 서버 runtime QA는 문서/하네스 마이그레이션 범위 밖이므로 실행하지 않는다.

## Observation Log

- 마이그레이션 시작 전 `bash scripts/validate-docs.sh`는 통과했다.
- 마이그레이션 시작 전 `docs/AGENT_LOOP.md`는 없었다.
- 마이그레이션 시작 전 active plan 2개에는 `Observation Log`와 `Validation Result` 섹션이 없었다.
- `docs/AGENT_LOOP.md`를 추가하고 `AGENTS.md`, `docs/index.md`, `docs/PLANS.md`, `docs/HANDOFF.md`에 연결했다.
- 기존 active plan 2개에는 완료 상태를 바꾸지 않고 `Observation Log`와 `Validation Result` 섹션만 추가했다.
- `scripts/validate-docs.sh`에 agent loop 문서, `Observation Log`, `Validation Result` 검사를 추가했다.
- 중간 검증에서 `bash scripts/validate-docs.sh`가 통과했다.
- `rg '<[A-Z_]+>' . --glob '!*.pyc' --glob '!__pycache__/**' --glob '!.venv/**' --glob '!chroma_db/**'`는 잔여 플레이스홀더를 보고하지 않았다.

## Open Work

- 없음.

## Completion

- Completed.
- `docs/AGENT_LOOP.md`를 추가했다.
- `/goal`, `/plan`, active exec plan, HANDOFF 관계를 `docs/PLANS.md`와 `docs/AGENT_LOOP.md`에 기록했다.
- RAG/eval tool observation과 validation 기록 기준을 문서화했다.
- 기존 active plan 2개는 active 상태로 유지하면서 새 검증 계약 섹션만 보강했다.
- active plan 관찰/검증 섹션을 `scripts/validate-docs.sh`로 검사하도록 했다.

## Validation Result

- 통과: `bash scripts/validate-docs.sh`
- 통과: `rg '<[A-Z_]+>' . --glob '!*.pyc' --glob '!__pycache__/**' --glob '!.venv/**' --glob '!chroma_db/**'`
- 미실행: 제품 코드 테스트, full eval, 서버 runtime QA
  - 이유: 이번 작업은 문서/하네스 마이그레이션 범위이며 제품 코드 변경이 없음.
