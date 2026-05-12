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
4. `docs/product-specs/terms-rag-system.md`
5. 관련 `docs/exec-plans/active/*`

## Operating Rules

- 리포지터리 밖에만 있는 지식은 없는 것으로 간주한다.
- 요구사항이 불명확하면 추정하지 말고 `Assumptions` 또는 `Open Questions`에 기록한다.
- 큰 작업은 구현 전에 `docs/exec-plans/active/`에 실행 계획을 먼저 남긴다.
- 작업 완료 시 완료 범위와 검증 결과를 계획 문서에 기록한다.
- 검증이 끝났고 남은 작업이 없으면 계획 문서를 `docs/exec-plans/completed/`로 이동한다.
- 커밋 후에는 `docs/HANDOFF.md`의 최근 반영 작업, 현재 상태, 다음 작업을 갱신한다.
- 구현 변경은 사용자가 명시적으로 승인한 경우에만 수행한다.
- 반복되는 규칙은 문서에 남기고 가능하면 스크립트나 테스트로 승격한다.

## Branch Strategy

- 새 구현 작업은 `feature/...`, `fix/...`, `docs/...` 작업 브랜치에서 시작한다.
- 브랜치 생성과 병합은 사용자가 승인한 뒤에만 수행한다.
- `main` 직접 작업은 예외적 상황에서만 허용한다.

## Key Docs

- 아키텍처 맵: `ARCHITECTURE.md`
- 문서 인덱스: `docs/index.md`
- 제품 명세: `docs/product-specs/terms-rag-system.md`
- 품질 기준: `docs/QUALITY_SCORE.md`
- 신뢰성 기준: `docs/RELIABILITY.md`
- 보안 기준: `docs/SECURITY.md`
