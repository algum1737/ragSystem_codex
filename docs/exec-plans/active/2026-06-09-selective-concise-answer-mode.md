# Selective Concise Answer Mode Plan

## Goal

기본 RAG 프롬프트를 교체하지 않고, 사용자가 빠른 요약 답변을 원할 때만 선택적으로 concise prompt를 적용하는 안전한 답변 모드를 설계한다.

## Scope

- `refined_concise_bullet` full eval 회귀 원인 정리
- API/CLI/UI에서 선택형 concise mode를 제공할지 설계
- no-answer 또는 평가 민감 케이스에는 기존 기본 프롬프트를 유지하는 라우팅 검토
- 구현 후보와 검증 계약 확정

## Out Of Scope

- 기본 프롬프트 즉시 교체
- 기본 모델 변경
- `top_k` 변경
- token cap 재도입
- GPU/systemd 설정 변경

## Assumptions

- `refined_concise_bullet` v4는 smoke 기준 빠르지만 full eval에서 `accuracy_mean=0.8804`, `not_found_success_rate=0.0`으로 회귀했다.
- 기존 기본 프롬프트는 품질 기준선 유지에 필요하다.
- 속도 개선은 운영 기본값 교체보다 사용자 선택형 또는 라우팅형 적용이 더 안전하다.

## Pre-flight checks

- `git status --short --branch`
- `docs/references/2026-06-09-refined-concise-bullet-prompt-result.md` 확인
- `api/models.py`, `api/main.py`, `query.py`, `app.py`의 query option 구조 확인
- `retriever/engine.py` 기본 프롬프트가 원복 상태인지 확인

## Steps

1. full eval 회귀 케이스를 분석한다.
2. 선택형 concise mode의 API/CLI/UI 인터페이스 후보를 정한다.
3. 기존 기본 프롬프트와 concise prompt를 안전하게 선택하는 구조를 설계한다.
4. 구현 여부와 검증 범위를 사용자에게 제안한다.

## Automated tests

- 설계 단계에서는 코드 변경 전이므로 문서 검증만 실행한다.
- 구현 승인 시 `.venv/bin/python -m py_compile retriever/engine.py api/models.py api/main.py query.py app.py`를 실행한다.
- 구현 승인 시 `bash scripts/validate-docs.sh`를 실행한다.

## Manual/Runtime QA

- 구현 승인 시 API smoke에서 기본 모드와 concise 모드를 각각 확인한다.
- concise 모드는 trace `total`, `llm`, `answer_length`를 기본 모드와 비교한다.
- 기본 모드는 no-answer 케이스 회귀가 없는지 확인한다.

## Skipped/Not Run

- full eval은 설계 단계에서는 실행하지 않는다.
- 구현 후 기본 모드 영향이 있으면 full eval을 실행한다.

## Open Work

- full eval 회귀 케이스 분석
- 선택형 concise mode 설계
