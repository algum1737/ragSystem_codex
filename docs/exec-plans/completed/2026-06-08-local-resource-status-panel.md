# Local Resource Status Panel Plan

## Goal

로컬 FastAPI와 Streamlit UI에 CPU/GPU/Ollama 적재 상태를 확인할 수 있는 리소스 상태 카테고리를 추가한다.

## Scope

- FastAPI에 `/runtime/resources` endpoint 추가
- CPU, RAM, GPU, Ollama 적재 모델 상태 수집
- Streamlit 시스템 탭에 리소스 상태 영역 추가
- 로컬 compile과 endpoint smoke 검증

## Out Of Scope

- 운영 서버 배포
- git commit 또는 PR 생성
- 장기 모니터링 저장소, 차트, 알림 기능
- GPU 설정 변경 또는 Ollama 설정 변경

## Assumptions

- 로컬 환경에는 `nvidia-smi`가 없을 수 있다.
- `ollama ps`는 모델이 idle unload 상태면 비어 있을 수 있다.
- `psutil`이 없으면 CPU/RAM은 unavailable로 표시한다.

## Pre-flight checks

- `git status --short --branch`
- `api/main.py`, `api/models.py`, `app.py` 기존 패턴 확인

## Steps

1. runtime resource 수집 helper를 API에 추가한다.
2. response model을 추가한다.
3. Streamlit 시스템 탭에서 `/runtime/resources`를 호출해 CPU/RAM/GPU/Ollama 상태를 표시한다.
4. 로컬 compile과 가능하면 API endpoint smoke를 실행한다.

## Automated tests

- `.venv/bin/python -m py_compile api/main.py api/models.py app.py`
- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 로컬 API 서버에서 `/runtime/resources`가 JSON을 반환하는지 확인
- Streamlit 시스템 탭에서 API 연결 실패 시에도 UI가 깨지지 않는지 확인

## Skipped/Not Run

- 운영 서버 배포는 하지 않는다.
- GPU가 없는 로컬 환경에서는 GPU unavailable 표시만 검증한다.

## Open Work

- 없음.

## Completion

- FastAPI에 `/runtime/resources` endpoint를 추가했다.
- endpoint는 CPU/RAM, `nvidia-smi` 기반 GPU 상태, `ollama ps` 기반 적재 모델 상태를 반환한다.
- `psutil`, `nvidia-smi`, `ollama`이 없거나 실패하는 환경에서는 unavailable 상태와 reason을 반환한다.
- Streamlit 시스템 탭에 `리소스 상태` 카테고리를 추가했다.
- 로컬 환경에서 API와 Streamlit을 기동해 smoke 검증을 완료했다.

## Validation Result

- 통과: `.venv/bin/python -m py_compile api/main.py api/models.py app.py`
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: 로컬 API `/runtime/resources`
  - CPU load, RAM 사용량, GPU unavailable, Ollama loaded 상태 JSON 반환 확인
- 통과: 로컬 API `/health`
  - `{"status":"ok","model":"gemma3:12b"}`
- 통과: Streamlit health
  - `http://127.0.0.1:8501/_stcore/health` 응답 `ok`
- 미실행: 브라우저 스크린샷 검증
  - 현재 세션에서 Browser 도구가 제공되지 않아 HTTP health와 API 호출 로그로 대체했다.
