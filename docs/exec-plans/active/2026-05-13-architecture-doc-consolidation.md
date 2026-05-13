# Architecture Document Consolidation Plan

## Goal

루트 `ARCHITECTURE.md`와 `docs/architecture.md`의 역할을 분리하거나 통합해 아키텍처 기준 문서의 중복을 줄인다.

## Scope

- 두 아키텍처 문서의 중복 내용 비교
- 유지할 canonical 문서 결정
- 참조 링크와 handoff 경로 갱신
- 문서 검증 스크립트 통과 확인

## Assumptions

- 루트 `ARCHITECTURE.md`는 Codex 작업자가 먼저 읽는 요약 문서로 유지할 가능성이 높다.
- `docs/architecture.md`는 원본 프로젝트에서 가져온 상세 문서일 수 있으므로 삭제 전 내용 비교가 필요하다.
- 구현 코드는 변경하지 않는다.

## Steps

1. `ARCHITECTURE.md`와 `docs/architecture.md`의 현재 내용을 비교한다.
2. 중복, 충돌, 보존해야 할 세부 정보를 분류한다.
3. canonical 문서와 보조 문서의 역할을 결정한다.
4. 필요한 문서 링크를 갱신한다.
5. `bash scripts/validate-docs.sh`로 검증한다.

## Risks

- 원본 상세 아키텍처 내용이 요약 과정에서 손실될 수 있다.
- 문서 링크를 일부 놓치면 다음 세션의 first-read 경로가 혼란스러워질 수 있다.

## Validation

- `bash scripts/validate-docs.sh`가 통과해야 한다.
- `rg "docs/architecture.md|ARCHITECTURE.md"` 결과에서 참조 의도가 명확해야 한다.
- completed 계획 링크와 active 계획 링크가 현재 상태와 일치해야 한다.

## Open Work

- 아키텍처 문서 중복 비교와 통합 방향 결정
- 링크 갱신
- 검증 실행
