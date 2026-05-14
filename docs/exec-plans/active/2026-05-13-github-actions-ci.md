# GitHub Actions CI Plan

## Goal

PR에서 checks가 비어 있는 문제를 해결하기 위해 GitHub Actions 기반 최소 CI를 추가한다.

## Scope

- `.github/workflows/ci.yml` 추가
- 문서 검증 실행
- Python 문법 검증 실행
- full eval은 로컬 런타임 의존성 때문에 CI 범위에서 제외

## Out Of Scope

- Ollama 기반 full eval CI 실행
- Hugging Face 모델 다운로드가 필요한 통합 테스트
- 브랜치 보호 규칙 설정

## Assumptions

- GitHub-hosted runner에는 로컬 Ollama와 Chroma 데이터가 없다.
- CI는 빠르고 안정적인 정적/문서 검증부터 시작한다.

## Pre-flight checks

- `.github/workflows/` 없음 확인 후 생성
- 로컬에서 `bash scripts/validate-docs.sh` 통과 확인
- 컴파일 대상 Python 파일 목록 확정: `eval/pipeline.py`, `retriever/engine.py`, `api/models.py`, `api/main.py`, `app.py`

## Steps

1. GitHub Actions workflow 파일을 추가한다.
2. PR과 main push에서 실행되도록 트리거를 설정한다.
3. 문서 검증과 Python compile 검증을 실행한다.
4. PR 생성 후 checks가 표시되는지 확인한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`

## Manual/Runtime QA

- PR 화면에서 checks가 생성되는지 확인한다.

## Skipped/Not Run

- full eval: Ollama, Chroma 데이터, 로컬 모델 캐시 의존성 때문에 CI에서 제외한다.

## Validation

- 로컬 문서 검증이 통과해야 한다.
- 로컬 Python compile 검증이 통과해야 한다.
- PR에서 GitHub Actions check가 보여야 한다.

## Validation Result

- 통과: `bash scripts/validate-docs.sh`
- 실패 후 대체 통과: `python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
  - 로컬 셸에 `python` 명령이 없어 `command not found`로 실패했다.
  - 동일 대상 파일을 `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`로 재실행해 통과했다.
- 미실행: PR 화면에서 GitHub Actions check 생성 확인
  - PR 생성 전이므로 아직 확인하지 못했다.

## Open Work

- PR 생성과 checks 확인
