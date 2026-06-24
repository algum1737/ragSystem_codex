# Agent Loop

이 문서는 Codex 스타일 에이전트 루프를 이 리포지터리의 RAG/eval 하네스 구조에 맞춰 해석한 운영 맵이다. 내부 런타임을 재구현하지 않고, 에이전트가 읽고 검증할 수 있는 프로젝트 상태를 리포지터리에 남기는 것이 목적이다.

## Loop Map

```text
User Intent
  -> Context Assembly
  -> Plan
  -> Tool Action
  -> Observation
  -> Validation
  -> Handoff
```

## Repository Mapping

| Loop stage | Repository surface | Purpose |
| --- | --- | --- |
| User Intent | 사용자 요청, `docs/product-specs/*`, eval 목표 | 목표, 제약, 품질 판단 기준을 고정한다. |
| Context Assembly | `AGENTS.md`, `README.md`, `ARCHITECTURE.md`, `docs/index.md`, `docs/HANDOFF.md` | 에이전트가 먼저 읽을 맥락을 제공한다. |
| Plan | `docs/exec-plans/active/*`, `/plan` | 구현 전에 범위, 단계, 검증 계약을 정한다. |
| Tool Action | shell, Python scripts, API/server checks, eval runner, trace/source drift tooling | 계획에 따라 파일 수정, 명령 실행, 평가 또는 관측 도구 호출을 수행한다. |
| Observation | tool output, eval results, trace summaries, source drift reports, `Observation Log` | 실행 결과와 실패 원인을 기록한다. |
| Validation | `scripts/validate-docs.sh`, py_compile, eval subset/full eval, runtime health checks | 완료 판단을 추측이 아니라 증거로 만든다. |
| Handoff | `docs/HANDOFF.md`, completed exec plan, `docs/references/*` | 다음 세션이 같은 상태에서 이어받게 한다. |

## Goal, Plan, And Repo State

- `/goal`은 현재 Codex 스레드 안의 지속 목표다.
- `/plan`은 구현 전 계획을 만들거나 다듬는 대화 모드다.
- `docs/exec-plans/active/*`는 리포지터리에 남는 실제 작업 계획과 검증 계약이다.
- `docs/HANDOFF.md`는 세션 전환, 컨텍스트 압축, 커밋 이후 재개를 위한 인계 상태다.

긴 작업은 `/goal`만으로 관리하지 않는다. 목표는 `/goal`에 둘 수 있지만, 실행 범위와 검증 결과는 active exec plan과 HANDOFF에 남긴다.

## Context Budget Rules

- `AGENTS.md`는 짧은 맵으로 유지하고 상세 설명은 `docs/`로 보낸다.
- active exec plan에는 현재 판단에 필요한 내용만 둔다.
- 완료된 계획은 `docs/exec-plans/completed/`로 이동한다.
- 긴 eval 결과, trace 분석, source drift 리포트는 plan 본문에 모두 붙이지 말고 `docs/references/`, `docs/generated/`, `eval/results/` 같은 산출물 경로로 분리한다.
- 불확실한 내용은 사실처럼 쓰지 않고 `Assumptions` 또는 `Open Questions`로 남긴다.

## Tool And Permission Rules

| Action type | Default rule |
| --- | --- |
| Read files, inspect docs, run status commands | 작업 맥락 확인을 위해 허용한다. |
| Edit files | 사용자 승인 후 수행한다. |
| Run docs validation, py_compile, focused eval, smoke checks | 변경 검증을 위해 수행하고 결과를 기록한다. |
| Full eval, server runtime checks, trace collection, source drift reports | 비용과 실행 시간을 plan에 적고 수행한다. |
| Network, package install, external API, MCP write action | 필요성과 위험을 설명하고 승인 또는 환경 정책을 따른다. |
| Destructive actions such as delete, reset, force push | 명시적 사용자 승인 없이는 수행하지 않는다. |

## Observation Contract

툴을 실행한 뒤에는 필요한 만큼 아래 정보를 남긴다.

- 실행한 명령 또는 도구
- 관찰한 결과
- 실패 또는 미실행 이유
- 재시도 여부
- 후속 작업 또는 남은 리스크

active exec plan의 `Observation Log`와 `Validation Result`는 이 계약을 기록하는 기본 위치다.

## Completion Criteria

작업 완료는 아래 조건을 모두 만족해야 한다.

- 목표 범위가 구현 또는 문서화됐다.
- 계획에 적은 검증이 실행됐거나, 미실행 사유가 기록됐다.
- RAG/eval 변경이면 관련 eval, trace, source drift, latency 영향이 기록됐다.
- 남은 작업이 있으면 `Open Work`에 판단 기준과 함께 남았다.
- 완료된 계획은 completed로 이동했고 `docs/index.md`와 `docs/HANDOFF.md`가 갱신됐다.
