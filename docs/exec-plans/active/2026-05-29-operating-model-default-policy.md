# Operating Model Default Policy Plan

## Goal

운영 서버에서 확인된 `gemma4:26b` 사용 상태와 코드 기본값 `gemma3:12b`, 기존 문서의 `gemma4:24b` 표현 사이의 차이를 정리하고 기본 모델 운영 정책을 결정한다.

## Scope

- 현재 코드 기본 모델 확인
- 서버 운영 모델 확인 결과 반영
- 기본 모델을 코드에 고정할지, systemd 후처리로 변경할지, UI/API 수동 변경 절차로 유지할지 결정
- 결정 결과를 배포 가이드와 handoff에 반영

## Out Of Scope

- 신규 LLM 품질 비교 평가
- 서버 GPU 드라이버 재설치
- Ollama 모델 다운로드

## Assumptions

- 운영 서버는 현재 `gemma4:26b`로 정상 응답한다.
- 코드 기본값은 아직 `gemma3:12b`다.
- 기본 모델 영구화는 운영 판단이 필요하다.

## Pre-flight checks

- `retriever/llm.py` 기본 모델 확인
- `docs/manual-deployment-guide.md`의 모델 관련 문구 확인
- 사용자 운영 모델 선호 확인

## Steps

1. 코드와 문서의 기본 모델 표현을 확인한다.
2. 운영 기본 모델 영구화 방식 후보를 비교한다.
3. 사용자 승인 후 코드 또는 문서 변경을 수행한다.
4. 검증과 handoff 갱신을 수행한다.

## Automated tests

- 변경 시 `bash scripts/validate-docs.sh`
- 코드 변경 시 `.venv/bin/python -m py_compile retriever/llm.py api/main.py app.py`

## Manual/Runtime QA

- 필요 시 서버에서 `/health` 모델 값 확인

## Skipped/Not Run

- 아직 운영 기본 모델 방식은 결정하지 않았다.

## Open Work

- `gemma4:26b`를 기본 운영 모델로 영구화할지 사용자 결정 필요.
