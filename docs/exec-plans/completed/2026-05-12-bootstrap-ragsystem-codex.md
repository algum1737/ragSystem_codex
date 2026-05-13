# Bootstrap And Migration Plan

## Goal

원본 `ragSystem` 프로젝트를 현재 저장소로 옮기고, `.paul` 중심 작업 기록 체계를 하네스 문서 구조로 전환한다.

## Scope

- 소스 코드와 일반 문서를 현재 저장소로 복사
- 런타임 산출물과 도구 전용 상태 디렉터리 제외
- 템플릿 기반 `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `docs/` 정비
- `.paul`의 프로젝트 정의, 상태, 로드맵을 하네스 문서로 재작성
- 최소 문서 검증 수행

## Assumptions

- 현재 저장소는 시작 시 비어 있었다.
- 원본 프로젝트의 `.paul`은 참고 자료로만 사용하고 직접 이식하지 않는다.
- 런타임 검증은 가상환경과 로컬 모델 준비 전에는 수행하지 않는다.

## Steps

1. `template-repo` 구조와 적용 규칙 확인
2. `ragSystem` 코드와 문서를 현재 저장소로 복사
3. 템플릿 `docs/`, `scripts/`, `.githooks/` 적용
4. 플레이스홀더 파일명을 실제 프로젝트 기준으로 치환
5. 상위 문서와 제품 명세를 현재 사실에 맞게 재작성
6. 문서 검증 스크립트 실행

## Risks

- 원본 프로젝트 문서와 새 하네스 문서가 중복될 수 있다.
- 런타임 산출물을 제외했기 때문에 즉시 실행은 불가능할 수 있다.
- 코드 내부 명칭과 제품 포지셔닝 문서가 완전히 동기화되지 않을 수 있다.

## Validation

- 필수 문서가 존재해야 한다.
- `AGENTS.md`는 짧은 맵으로 유지되어야 한다.
- 실행 계획과 제품 명세 문서가 연결되어야 한다.
- 제품 명세는 현재 코드와 알려진 사실과 충돌하지 않아야 한다.
- `bash scripts/validate-docs.sh`가 통과해야 한다.

## Progress

- `template-repo` 구조 확인 완료
- `ragSystem` 코드 복사 완료
- `docs/`, `scripts/`, `.githooks/` 적용 완료
- 플레이스홀더 치환 완료
- 상위 문서 재작성 완료
- `bash scripts/validate-docs.sh` 통과
- 플레이스홀더 검색 `rg '<[A-Z_]+>' .` 결과 없음
- Git 초기화와 초기 기준 커밋 완료

## Completion

- 완료일: 2026-05-13
- 런타임 검증 범위는 `2026-05-12-runtime-validation.md`로 분리했다.
- 가상환경, API, Streamlit, 평가 스크립트 검증은 후속 runtime validation 계획에서 완료했다.
- 남은 작업 없음.
