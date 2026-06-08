# Concise Answer Prompt Experiment Plan

## Goal

`gemma3:12b + top_k=5` 운영 조합에서 답변 길이를 줄여 LLM 생성 시간을 낮출 수 있는 concise-answer prompt 후보를 검증한다.

## Scope

- 현재 프롬프트 구조 확인
- 대표 질의 2-3건 기준 concise prompt 후보 설계
- 답변 길이, LLM latency, total latency, source 수, 품질 리스크 비교
- 채택 여부 판단

## Out Of Scope

- 운영 서버 즉시 배포
- 기본 모델 변경
- `top_k` 변경
- token cap 재도입
- GPU/systemd 설정 변경

## Assumptions

- 현재 운영 기본 모델은 `gemma3:12b`다.
- 현재 기본 `top_k`는 5다.
- token cap은 이전 실험에서 답변 절단 또는 실익 부족으로 채택하지 않았다.
- 다음 속도 병목은 LLM 생성 길이와 답변 형식이다.

## Pre-flight checks

- `git status --short --branch`
- 현재 active plan 확인
- `retriever/engine.py`, `retriever/llm.py` 프롬프트 경로 확인
- 최근 trace 기준 대표 질의와 latency 확인

## Steps

1. 현재 RAG 프롬프트와 답변 형식을 확인한다.
2. concise prompt 후보를 1-2개 만든다.
3. 대표 질의에서 baseline과 후보를 비교한다.
4. latency와 품질 리스크를 문서화한다.
5. 채택 여부와 다음 작업을 결정한다.

## Automated tests

- `.venv/bin/python -m py_compile retriever/engine.py retriever/llm.py query.py api/main.py app.py`
- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 또는 로컬 CLI/API 대표 질의 smoke
- trace `total`, `retrieval_total`, `llm`, `answer_length` 비교
- 답변이 근거를 유지하고 과도하게 절단되지 않는지 확인

## Skipped/Not Run

- full eval은 후보 smoke에서 채택 가능성이 확인된 뒤 별도 판단한다.
- 운영 배포는 이번 실험 결과에 따라 별도 승인 후 진행한다.

## Open Work

- 프롬프트 구조 확인
- 후보 설계 및 smoke 비교
