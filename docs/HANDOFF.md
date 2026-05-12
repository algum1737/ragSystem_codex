# Handoff

이 문서는 다음 세션이 현재 상태를 빠르게 이어받기 위한 인계 문서다.

## Read First

1. `AGENTS.md`
2. `README.md`
3. `ARCHITECTURE.md`
4. `docs/index.md`
5. `docs/PLANS.md`
6. `docs/product-specs/terms-rag-system.md`
7. `docs/exec-plans/active/2026-05-12-bootstrap-ragsystem-codex.md`

## Current Baseline

- 현재 브랜치: `git branch --show-current`로 확인
- 기준 커밋: `git rev-parse --short HEAD`로 확인
- 제품/서비스: 로컬 RAG 기반 문서 초안 생성 시스템
- 현재 상태: `ragSystem` 소스 복사, 하네스 문서 전환, 초기 기준 커밋 생성 완료
- 주요 목표: `.paul` 기반 운영 지식을 `docs/` 체계로 옮기고 이후 개선 작업을 Codex 방식으로 이어간다

## Working Rules

- 큰 작업은 구현 전에 `docs/exec-plans/active/`에 실행 계획을 작성한다.
- 작업 완료 시 완료 범위, 남은 작업 여부, 검증 결과를 계획 문서에 남긴다.
- 완료된 계획은 `docs/exec-plans/completed/`로 이동하고 `docs/index.md`와 이 문서를 갱신한다.
- 구현 변경은 사용자가 명시적으로 승인한 경우에만 수행한다.
- 새 실제 작업은 `main`에서 직접 하지 않고 작업 브랜치에서 진행한다.
- 커밋 해시는 이 문서에 고정하지 말고 git 명령으로 확인하게 유지한다.

## Recent Progress

- `ragSystem` 프로젝트 코드를 현재 저장소로 복사했다.
- `.venv`, `chroma_db`, 로그, `.paul`, `.claude` 같은 런타임 또는 도구별 상태 디렉터리는 제외했다.
- `template-repo` 기반 `docs/`, `scripts/`, `.githooks/` 골격을 적용했다.
- `.paul`의 프로젝트 정의와 로드맵을 `README.md`, `ARCHITECTURE.md`, `docs/PLANS.md`, 제품 명세와 실행 계획으로 재구성했다.
- `bash scripts/validate-docs.sh` 통과와 플레이스홀더 제거 확인을 마쳤다.
- Git 저장소를 초기화하고 초기 기준 커밋을 만들었다.

## Current Gaps

- 현재 폴더에 `.git`이 없어 브랜치/커밋 기반 handoff 루프는 아직 활성화되지 않았다.
- Python 가상환경과 의존성 설치는 아직 수행하지 않았다.
- 서버 기동, API, Streamlit, 평가 스크립트의 런타임 검증은 아직 하지 않았다.
- 코드 내부의 명칭과 문서 상 제품 정의 사이에 일부 정리되지 않은 표현이 남아 있다.

## Suggested Next Work

1. 다음 실제 작업용 브랜치를 만든다.
2. `python3 -m venv .venv`와 `pip install -r requirements.txt`로 실행 환경을 복구한다.
3. `uvicorn api.main:app --port 8000`, `streamlit run app.py`, `python eval/pipeline.py --metric retrieval` 기준의 실제 검증 계획을 만든다.
4. `docs/architecture.md`와 `ARCHITECTURE.md`의 중복을 정리하고 장기적으로 하나의 아키텍처 소스로 통합한다.

## Handoff Prompt

```text
이 프로젝트는 하네스 엔지니어링 방식으로 진행 중이다.

먼저 아래 파일을 읽고 현재 상태를 요약해라.
1. AGENTS.md
2. README.md
3. ARCHITECTURE.md
4. docs/index.md
5. docs/PLANS.md
6. docs/product-specs/terms-rag-system.md
7. docs/exec-plans/active/2026-05-12-bootstrap-ragsystem-codex.md

현재 기준:
- branch: `git branch --show-current`
- commit: `git rev-parse --short HEAD`

작업 규칙:
- 큰 작업은 active exec plan을 먼저 작성해라.
- 작업 완료 시 완료 범위와 검증 결과를 기록하고 completed로 이동해라.
- 커밋 후에는 docs/HANDOFF.md를 갱신하되, 커밋 해시는 git 명령으로 확인하게 유지해라.
```
