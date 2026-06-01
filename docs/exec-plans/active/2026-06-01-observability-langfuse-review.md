# Observability And Langfuse Review Plan

## Goal

현재 자체 eval/log 기반 운영 방식에 Langfuse 같은 LLM observability 도구를 붙일 필요가 있는지 검토하고, 도입한다면 최소 연동 범위를 정한다.

## Scope

- 현재 관측 방식 정리: eval JSON, source drift report, FastAPI/systemd logs
- Langfuse 또는 유사 도구 도입 후보 검토
- 추적 대상 정의: query, retrieved sources, prompt, model, latency, token/response, eval score
- 보안/운영 리스크 검토: 약관 문서, 사용자 질의, 내부 서버 네트워크
- 도입 여부와 1차 구현 범위 결정

## Out Of Scope

- 즉시 외부 SaaS 연동
- 운영 데이터 외부 전송
- 대규모 UI 변경

## Assumptions

- 현재 프로젝트에는 Langfuse가 연동되어 있지 않다.
- 운영 서버는 내부망이며, 관측 도구 도입 시 데이터 반출 여부가 핵심 판단 기준이다.
- 먼저 self-hosted 또는 로컬 저장 방식 가능성을 검토한다.

## Pre-flight checks

- 현재 logging/eval/report 구조 확인
- API query path와 RAGEngine query path 확인
- 민감 데이터 포함 가능성 확인

## Steps

1. 현재 관측 가능 항목과 부족한 항목을 정리한다.
2. Langfuse 도입 시 추적해야 할 이벤트 스키마를 설계한다.
3. self-hosted/SaaS/도입 보류 옵션을 비교한다.
4. 결정 내용을 참조 문서와 handoff에 기록한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 운영 서버와 데이터 반출 조건을 사람이 검토한다.

## Skipped/Not Run

- 아직 Langfuse 연동 구현은 수행하지 않는다.

## Open Work

- Langfuse 또는 유사 observability 도구 도입 여부 검토.
