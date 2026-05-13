# Plans

## Rules

- 큰 작업은 구현 전에 반드시 `exec-plans/active/`에 실행 계획을 만든다.
- 실행 계획은 목표, 범위, 가정, 단계, 리스크, 검증 방법, 남은 작업 여부를 포함한다.
- 진행 중 계획은 `exec-plans/active/`에 둔다.
- 작업이 완료되면 완료 범위와 검증 결과를 계획 문서에 기록한다.
- 검증 기준을 충족하고 남은 작업이 없으면 계획 문서를 `exec-plans/completed/`로 이동한다.
- 계획을 이동할 때는 `docs/index.md`와 `docs/HANDOFF.md`도 함께 갱신한다.
- 완료됐는지 애매한 작업은 `active/`에 남기되 `Open Work`와 다음 판단 기준을 적는다.

## Current Roadmap

### Bootstrap

- `2026-05-12-bootstrap-ragsystem-codex.md`
  - 목표: 소스 프로젝트와 하네스 운영 체계를 결합한다.
  - 상태: Completed

### Runtime Validation

- `2026-05-12-runtime-validation.md`
  - 목표: 실행 환경을 복구하고 API, UI, eval smoke test를 수행한다.
  - 상태: Completed

### Cross-Encoder Offline Setup

- `2026-05-13-cross-encoder-offline.md`
  - 목표: reranking 모델 캐시를 준비해 완전 오프라인 경로를 맞춘다.
  - 상태: Completed

### Follow-Up Candidates

- 런타임 환경 복구와 smoke test 계획
- 평가 파이프라인 실제 실행과 기준선 재확인
- 문서 명칭 정리와 아키텍처 문서 통합
- Phase 14 수준의 정확도와 faithfulness 평가 계획 재수립

## Active Plans

- `exec-plans/active/2026-05-13-architecture-doc-consolidation.md`

## Completed Plans

- `exec-plans/completed/2026-05-12-bootstrap-ragsystem-codex.md`
- `exec-plans/completed/2026-05-12-runtime-validation.md`
- `exec-plans/completed/2026-05-13-cross-encoder-offline.md`
