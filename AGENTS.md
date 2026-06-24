# AGENTS.md

이 파일은 이 리포지터리의 짧은 작업 맵이다. 세부 규칙은 `docs/`에서 찾는다.

## Mission

- 목표는 로컬 RAG 문서 생성 시스템과 이를 지속적으로 유지할 수 있는 하네스를 함께 구축하는 것이다.
- 사람은 방향, 우선순위, 승인, 제품 판단을 담당한다.
- 에이전트는 설계, 구현, 테스트, 문서화, 검증, 정리 작업을 수행한다.

## First Reads

작업 시작 전 아래 순서로 읽는다.

1. `README.md`
2. `ARCHITECTURE.md`
3. `docs/index.md`
4. `docs/AGENT_LOOP.md`
5. `docs/product-specs/terms-rag-system.md`
6. 관련 `docs/exec-plans/active/*`

## Operating Rules

- 우선순위는 사용자 명시 지시, 이 `AGENTS.md`, `docs/` 하네스 문서, 설치된 Superpowers skill, 기본 에이전트 동작 순서다.
- 리포지터리 밖에만 있는 지식은 없는 것으로 간주한다.
- 요구사항이 불명확하면 추정하지 말고 `Assumptions` 또는 `Open Questions`에 기록한다.
- 큰 작업은 구현 전에 `docs/exec-plans/active/`에 실행 계획을 먼저 남긴다.
- 작업 완료 시 완료 범위와 검증 결과를 계획 문서에 기록한다.
- 검증이 끝났고 남은 작업이 없으면 계획 문서를 `docs/exec-plans/completed/`로 이동한다.
- exec plan에는 작업 시작 전에 검증 계약을 고정한다. 최소한 `Pre-flight checks`, `Automated tests`, `Manual/Runtime QA`, `Skipped/Not Run` 판단 기준을 명시하고 완료 시 `Validation Result`에서 실행/통과/실패/미실행과 이유를 대조한다.
- Superpowers가 설치된 환경에서는 관련 workflow skill을 사용한다. 요구사항 정리는 `brainstorming`, 구현 계획은 `writing-plans`, 기능/버그 구현은 `test-driven-development`, 버그 분석은 `systematic-debugging`, 완료 전 확인은 `verification-before-completion`을 우선 검토한다.
- Superpowers 기본 저장 경로보다 이 리포지터리의 경로를 우선한다. 스펙과 실행 계획은 가능한 한 `docs/product-specs/`, `docs/design-docs/`, `docs/exec-plans/active/`에 남긴다.
- 커밋 후에는 `docs/HANDOFF.md`의 최근 반영 작업, 현재 상태, 다음 작업을 갱신한다.
- 구현 변경은 사용자가 명시적으로 승인한 경우에만 수행한다.
- 반복되는 규칙은 문서에 남기고 가능하면 스크립트나 테스트로 승격한다.

## Branch Strategy

- 새 구현 작업은 `feature/...`, `fix/...`, `docs/...` 작업 브랜치에서 시작한다.
- 브랜치 생성과 병합은 사용자가 승인한 뒤에만 수행한다.
- `main` 직접 작업은 예외적 상황에서만 허용한다.

## Pull Request Workflow

- PR 생성이 필요한 경우 `gh pr create`로 직접 생성한다.
- PR 제목과 본문은 한국어로 작성한다.
- PR 본문에는 요약, 변경 사항, 검증 결과, 평가 결과가 있으면 해당 지표, 남은 작업을 포함한다.
- `gh` 사용이 불가능한 경우에만 PR 생성 링크와 입력 내용을 사용자에게 제공한다.

## Output Expectations

- 변경에는 목적, 이유, 검증 방법이 있어야 한다.
- 제품 코드보다 먼저 작업 환경과 검증 루프를 정리한다.
- 문서만 제안하지 말고 강제 가능한 항목은 스크립트나 CI 후보로 표시한다.

## Key Docs

- 아키텍처 맵: `ARCHITECTURE.md`
- 문서 인덱스: `docs/index.md`
- 에이전트 루프: `docs/AGENT_LOOP.md`
- 제품 명세: `docs/product-specs/terms-rag-system.md`
- 품질 기준: `docs/QUALITY_SCORE.md`
- 신뢰성 기준: `docs/RELIABILITY.md`
- 보안 기준: `docs/SECURITY.md`
- Superpowers 연동: `docs/references/superpowers.md`
