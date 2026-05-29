# Ubuntu Server Runtime Verification Plan

## Goal

머지된 배포 호환 변경을 기준으로 Ubuntu 서버 런타임 상태를 재확인하고 필요한 후속 운영 작업을 정리한다.

## Scope

- FastAPI와 Streamlit 서비스 상태 확인 절차 정리
- GPU/PyTorch CUDA 조합 확인 결과 기록 여부 판단
- `gemma4:26b` 운영 모델 적용 방식 확인
- 필요 시 서버 재배포 또는 systemd 보강 작업 계획화

## Out Of Scope

- 서버 직접 재설치
- 신규 평가 케이스 추가
- 검색 알고리즘 변경

## Assumptions

- PR #28은 main에 머지됐다.
- Ubuntu 서버는 수동 배포 상태이며, 운영 확인은 별도 승인과 서버 접근 상태에 따른다.

## Pre-flight checks

- `git status --short --branch` 확인
- `docs/manual-deployment-guide.md` 최신 절차 확인
- 서버 서비스 상태 확인 가능 여부 확인

## Steps

1. 로컬 main과 origin/main 동기화 상태를 확인한다.
2. 서버에서 `ragsystem-api`, `ragsystem-web`, `ollama` 상태 확인 절차를 실행할지 결정한다.
3. GPU/PyTorch CUDA 상태와 `gemma4:26b` 모델 적용 상태를 확인한다.
4. 필요 시 운영 자동화 또는 기본 모델 영구화 작업을 별도 계획으로 분리한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버에서 `curl http://localhost:8000/health`와 Streamlit 접속 확인
- 서버에서 실제 쿼리탭 응답 확인

## Skipped/Not Run

- 브라우저 수동 조작은 실행하지 않았다. 대신 Streamlit 포트의 HTTP 200과 API 쿼리 응답으로 런타임 상태를 확인했다.

## Completion

- 서버 `srv01`에서 `ragsystem-api`, `ragsystem-web`, `ollama`가 모두 `active`임을 확인했다.
- `GET http://localhost:8000/health`는 `status=ok`, `model=gemma4:26b`를 반환했다.
- `GET http://localhost:8000/stats`는 `collection_name=ragSystem`, `count=318`을 반환했다.
- PyTorch는 `2.3.1+cu118`, CUDA runtime은 `11.8`, GPU는 `NVIDIA GeForce RTX 2080 Ti`로 인식됐다.
- 위치기반서비스 분쟁 해결 질의에 대해 `POST /query`가 HTTP 200과 5개 source를 반환했고, 쿼리 후 API 서비스가 계속 `active` 상태임을 확인했다.
- Streamlit `http://localhost:8501`은 HTTP 200을 반환했다.

## Validation Result

- 통과: `ssh ragadmin.10.220.5 systemctl is-active ragsystem-api ragsystem-web ollama`
- 통과: `curl http://localhost:8000/health`
- 통과: `curl http://localhost:8000/stats`
- 통과: 서버 가상환경 PyTorch CUDA 확인
- 통과: 위치기반서비스 분쟁 해결 RAG query API 응답 확인
- 통과: Streamlit HTTP 200 확인

## Open Work

- 운영 서버는 현재 `gemma4:26b`로 동작한다. 코드 기본값과 문서의 `gemma4:26b` 표현을 운영 모델 정책으로 정리해야 한다.
