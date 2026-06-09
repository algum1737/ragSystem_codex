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

- 없음. 구현과 서버 검증까지 완료했다.

## Progress

- `api/models.py`, `api/main.py`, `query.py`, `app.py`, `retriever/engine.py`의 query option 구조를 확인했다.
- full eval 실패 리포트 `/opt/ragSystem_codex/eval/results/eval_20260609_095553.json`을 분석했다.
- 회귀는 expected no-answer 1건뿐 아니라 keyword 누락/혼입 6건도 포함했다.
- 자동 라우팅은 v1에서 배제하고, 사용자 명시 선택형 `answer_mode=standard|concise` 설계로 정했다.
- 설계 결과는 `docs/references/2026-06-09-selective-concise-answer-mode-design.md`에 기록했다.

## Interim Decision

- 기본값은 `standard`로 유지한다.
- `concise`는 명시적 요청에서만 실행한다.
- module-level `PROMPT_TEMPLATE`를 요청마다 바꾸지 않고, `RAGEngine.query(answer_mode=...)`에서 per-call prompt를 선택한다.
- trace metadata에 `answer_mode`를 기록한다.
- 구현 승인 시 API, CLI, Streamlit에 선택형 모드를 추가한다.

## Interim Validation Result

- 통과: active plan 확인
- 통과: API/CLI/UI query option 구조 확인
- 통과: full eval 실패 케이스 분석
- 통과: 설계 문서 작성
- 통과: 선택형 concise mode 구현
- 통과: 로컬 compile
- 통과: 서버 compile
- 통과: 서버 API/Web 재기동 및 health 확인
- 통과: API standard/concise smoke
- 통과: standard full eval
  - 리포트: `/opt/ragSystem_codex/eval/results/eval_20260609_110223.json`
  - `accuracy_mean=0.9891`
  - `faithfulness_mean=0.9565`
  - `not_found_success_rate=1.0`

## Completion

- `answer_mode=standard|concise` 선택형 답변 모드를 구현했다.
- 기본값은 `standard`이며 기존 기본 프롬프트를 유지한다.
- `concise`는 명시적 요청에서만 refined concise bullet prompt를 사용한다.
- API, CLI, Streamlit UI에 선택형 모드를 연결했다.
- trace metadata에 `answer_mode`를 기록한다.
- 서버 배포와 smoke를 완료했다.
- 결과 문서는 `docs/references/2026-06-09-selective-concise-answer-mode-result.md`에 기록했다.
