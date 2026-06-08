# Server Resource Panel Deploy Plan

## Goal

로컬에서 구현한 CPU/GPU/Ollama 리소스 상태 패널과 GPU 사용량 heatmap을 Ubuntu 서버에 반영하고 런타임에서 동작을 확인한다.

## Scope

- `api/main.py`, `api/models.py`, `app.py`를 서버 `/opt/ragSystem_codex`에 반영
- 서버 Python compile 검증
- FastAPI와 Streamlit 서비스 재시작
- `/runtime/resources`, `/runtime/resources/history`, `/health`, Streamlit health 확인

## Out Of Scope

- git commit 또는 PR 생성
- 운영 모델 변경
- GPU/Ollama/systemd 설정 변경
- 장기 모니터링 저장소 또는 알림 기능

## Assumptions

- 서버 배포 경로는 `/opt/ragSystem_codex`다.
- 서버 접속 계정은 기존 작업과 동일하게 `ragadmin@10.10.220.5`다.
- 서버에는 `nvidia-smi`가 있어 GPU별 사용률과 VRAM 히스토리가 표시될 수 있다.
- 리소스 히스토리는 API 프로세스 메모리에만 저장되며 재시작 시 초기화된다.

## Pre-flight checks

- `git status --short --branch`
- 서버 `/opt/ragSystem_codex` 존재 확인
- 서버 서비스 상태 확인

## Steps

1. 서버 대상 경로와 서비스 상태를 확인한다.
2. 런타임 코드 3개 파일을 서버에 복사한다.
3. 서버 venv에서 compile 검증을 실행한다.
4. FastAPI와 Streamlit을 재시작한다.
5. health, resource endpoint, Streamlit health를 확인한다.

## Automated tests

- 서버: `.venv/bin/python -m py_compile api/main.py api/models.py app.py`
- 로컬: `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 `/health`
- 서버 `/runtime/resources`
- 서버 `/runtime/resources/history`
- Streamlit HTTP health
- 필요 시 `ollama ps`, `nvidia-smi`

## Skipped/Not Run

- 실제 브라우저 스크린샷 검증은 도구가 제공되는 경우에만 수행한다.
- git commit/push는 하지 않는다.

## Open Work

- 없음.

## Completion

- `api/main.py`, `api/models.py`, `app.py`를 서버 `/opt/ragSystem_codex`에 반영했다.
- systemd 서비스 PATH가 venv로 제한되어 `/usr/bin/nvidia-smi`, `/usr/local/bin/ollama`를 찾지 못하는 문제를 확인했다.
- 앱 코드에서 `nvidia-smi`, `ollama` 명령의 표준 절대 경로 fallback을 추가하고 서버에 재반영했다.
- 서버 FastAPI와 Streamlit 서비스를 재시작해 새 코드를 적용했다.
- 서버에서 GPU 2장과 Ollama 적재 모델 상태가 `/runtime/resources`에 표시되는 것을 확인했다.
- 대표 RAG 질의 실행 중 GPU history에 실제 사용률/VRAM 샘플이 기록되는 것을 확인했다.

## Validation Result

- 통과: 서버 compile
  - `cd /opt/ragSystem_codex && .venv/bin/python -m py_compile api/main.py api/models.py app.py`
- 통과: 서비스 재시작
  - `ragsystem-api.service`: active, PID 갱신 확인
  - `ragsystem-web.service`: active, PID 갱신 확인
- 통과: 서버 `/health`
  - `{"status":"ok","model":"gemma3:12b"}`
- 통과: 서버 `/runtime/resources`
  - CPU/RAM 반환 확인
  - GPU 0/1: `NVIDIA GeForce RTX 2080 Ti`
  - Ollama: `gemma3:12b`, `100% GPU`, context `4096`
- 통과: 서버 `/runtime/resources/history`
  - `interval_seconds=5`, `max_samples=720`
  - idle 샘플과 RAG 질의 중 GPU 사용 샘플 누적 확인
  - 질의 중 샘플 예: GPU 1 utilization `87.0%`, GPU 0 VRAM `31.3%`, GPU 1 VRAM `81.3%`
- 통과: Streamlit health
  - `http://10.10.220.5:8501/_stcore/health` 응답 `ok`
- 통과: 로컬 검증
  - `.venv/bin/python -m py_compile api/main.py api/models.py app.py`
  - `bash scripts/validate-docs.sh`
- 미실행: 브라우저 스크린샷 검증
  - 현재 세션에서 Browser 도구가 제공되지 않아 HTTP health와 API endpoint 결과로 대체했다.
