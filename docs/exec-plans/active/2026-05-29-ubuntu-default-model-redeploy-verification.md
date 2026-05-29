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

- 아직 서버 재배포 확인은 실행하지 않았다.

## Open Work

- 서버 배포본 갱신 및 재시작 검증 필요 여부 확인.
