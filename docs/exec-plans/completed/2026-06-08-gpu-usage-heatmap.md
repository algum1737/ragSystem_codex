# GPU Usage Heatmap Plan

## Goal

Streamlit 시스템 탭에서 GitHub contributions 그래프처럼 GPU별 사용량 히스토리를 heatmap으로 확인할 수 있게 한다.

## Scope

- FastAPI에 GPU 리소스 샘플 히스토리 ring buffer 추가
- `/runtime/resources/history` endpoint 추가
- Streamlit 시스템 탭에 GPU 사용률/VRAM 선택 heatmap 추가
- GPU가 없는 로컬 환경에서는 unavailable 상태를 유지하되 endpoint/UI가 깨지지 않게 처리

## Out Of Scope

- 운영 서버 배포
- git commit 또는 PR 생성
- 영구 저장소 기반 장기 메트릭 보관
- 알림, 임계치 경보, Prometheus/Grafana 연동

## Assumptions

- 현재 로컬 Mac에는 `nvidia-smi`가 없으므로 실제 GPU heatmap 데이터는 비어 있을 수 있다.
- Ubuntu 서버에서는 `nvidia-smi`가 있으면 GPU별 utilization과 VRAM history가 표시된다.
- 히스토리는 API 프로세스 메모리에만 보관하며 재시작 시 초기화된다.

## Pre-flight checks

- `git status --short --branch`
- 현재 `/runtime/resources` endpoint 구현 확인
- Streamlit 시스템 탭 리소스 상태 UI 확인

## Steps

1. FastAPI에서 resource sample을 history buffer에 기록한다.
2. `/runtime/resources/history` endpoint를 추가한다.
3. Streamlit에 metric 선택과 GPU별 heatmap 렌더링을 추가한다.
4. 로컬 compile, docs validation, endpoint smoke를 실행한다.

## Automated tests

- `.venv/bin/python -m py_compile api/main.py api/models.py app.py`
- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 로컬 `/runtime/resources/history` JSON 응답 확인
- Streamlit health 확인
- GPU 미지원 환경에서 UI가 fallback 메시지를 표시하는지 확인

## Skipped/Not Run

- 실제 GPU가 있는 Ubuntu 서버 검증은 이번 로컬 작업 범위에서 제외한다.
- 브라우저 스크린샷 검증은 도구가 제공되는 경우에만 수행한다.

## Open Work

- 없음.

## Completion

- FastAPI에 메모리 기반 리소스 히스토리 ring buffer를 추가했다.
- API 시작 시 5초 주기로 GPU 샘플을 수집하는 background sampler를 추가했다.
- `/runtime/resources/history` endpoint를 추가했다.
- Streamlit 시스템 탭에 GPU 사용률/VRAM 사용률 선택형 heatmap을 추가했다.
- GPU가 없는 로컬 환경에서는 `nvidia-smi not found` 상태와 빈 GPU history를 정상 fallback으로 표시한다.

## Validation Result

- 통과: `.venv/bin/python -m py_compile api/main.py api/models.py app.py`
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: 로컬 API `/runtime/resources`
  - CPU/RAM/Ollama/GPU unavailable JSON 반환 확인
- 통과: 로컬 API `/runtime/resources/history`
  - `interval_seconds=5`, `max_samples=720`, 샘플 누적 확인
- 통과: Streamlit health
  - `http://127.0.0.1:8501/_stcore/health` 응답 `ok`
- 미실행: 실제 GPU heatmap 데이터 확인
  - 로컬 Mac 환경에는 `nvidia-smi`가 없어 실제 GPU별 utilization/VRAM 샘플은 Ubuntu 서버 반영 후 확인해야 한다.
