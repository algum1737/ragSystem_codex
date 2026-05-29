# Ubuntu Default Model Redeploy Verification Plan

## Goal

코드 기본 모델을 `gemma4:26b`로 변경한 뒤, Ubuntu 서버 재배포 또는 서비스 재시작 시 기본 모델이 의도대로 적용되는지 확인한다.

## Scope

- 로컬 main의 기본 모델 변경 상태 확인
- 서버 배포본 갱신 필요 여부 판단
- `ragsystem-api` 재시작 후 `/health` 모델 값 확인
- 필요 시 systemd 또는 배포 절차 보강

## Out Of Scope

- 신규 모델 품질 평가
- Ollama 모델 다운로드
- GPU 드라이버 변경

## Assumptions

- 운영 서버에는 `gemma4:26b`가 이미 설치되어 있고 현재 정상 응답한다.
- 코드 기본값 변경은 아직 서버 배포본에 반영되지 않았을 수 있다.

## Pre-flight checks

- `git status --short --branch` 확인
- 서버 `/health` 모델 값 확인
- 서버 배포본의 `retriever/llm.py` 기본값 확인

## Steps

1. 원격 main과 로컬 main 동기화 상태를 확인한다.
2. 서버 배포본에 기본 모델 변경이 반영됐는지 확인한다.
3. 필요하면 수동 배포 절차에 따라 서버 배포본을 갱신한다.
4. `ragsystem-api` 재시작 후 `/health`가 `gemma4:26b`를 반환하는지 확인한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버에서 `curl http://localhost:8000/health` 확인
- 필요 시 실제 RAG 쿼리 1건 확인

## Skipped/Not Run

- 없음. 서버 배포본 갱신, 서비스 재기동, health/stats/query/web 확인을 수행했다.

## Completion

- 로컬 main과 origin/main이 `d74a822`로 일치함을 확인했다.
- 서버 배포본의 `retriever/llm.py`가 기존 `gemma3:12b` 기본값 상태임을 확인했다.
- `.venv`와 `chroma_db`를 제외한 최신 코드 압축본을 서버에 업로드하고 `/opt/ragSystem_codex`에 반영했다.
- 서버 배포본의 `DEFAULT_MODEL = "gemma4:26b"` 반영을 확인했다.
- `ragsystem-api`, `ragsystem-web`, `ollama`가 재기동 후 active 상태임을 확인했다.
- `/health`는 `model=gemma4:26b`, `/stats`는 `count=318`, Streamlit은 HTTP 200을 반환했다.
- 실제 RAG query 1건이 HTTP 응답과 5개 source를 반환했다.

## Validation Result

- 통과: `git status --short --branch`
- 통과: 서버 배포본 `DEFAULT_MODEL = "gemma4:26b"` 확인
- 통과: `curl http://localhost:8000/health` -> `{"status":"ok","model":"gemma4:26b"}`
- 통과: `curl http://localhost:8000/stats` -> `{"collection_name":"ragSystem","count":318}`
- 통과: Streamlit HTTP 200
- 통과: 실제 RAG query 1건 응답 및 5개 source 확인
- 주의: `sudo systemctl restart`는 비대화형 SSH에서 sudo 암호를 요구해 직접 실행하지 못했다. 대신 `ragadmin` 소유 API/Web 프로세스를 종료했고 systemd `Restart=always` 정책으로 재기동됨을 확인했다.

## Open Work

- 없음.
