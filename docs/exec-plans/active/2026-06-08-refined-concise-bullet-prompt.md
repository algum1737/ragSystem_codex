# Refined Concise Bullet Prompt Plan

## Goal

`gemma3:12b + top_k=5` 운영 조합에서 `concise_bullet` 실험 결과를 바탕으로 답변 길이를 줄이되, 불필요한 no-answer 문장과 source drift를 줄인 운영 프롬프트 후보를 적용 가능 수준으로 검증한다.

## Scope

- `concise_bullet` 후보의 forced no-answer bullet 규칙 완화
- 기본 RAG 프롬프트 후보 문구 작성
- 대표 질의 smoke 비교
- 필요 시 full eval 실행
- 채택 가능 시 사용자 승인 후 코드 반영 및 서버 배포

## Out Of Scope

- 기본 모델 변경
- `top_k` 변경
- token cap 재도입
- GPU/systemd 설정 변경
- 사용자 승인 없는 운영 기본 프롬프트 변경

## Assumptions

- 현재 운영 기본 모델은 `gemma3:12b`다.
- 현재 기본 `top_k`는 5다.
- 직전 실험에서 latency 병목은 retrieval이 아니라 LLM 생성 길이로 확인됐다.
- `concise_summary`는 더 빠르지만 품질 리스크가 있어 1차 적용 후보에서 제외한다.

## Pre-flight checks

- `git status --short --branch`
- `docs/references/2026-06-08-concise-answer-prompt-experiment-result.md` 확인
- `retriever/engine.py` 기본 프롬프트 확인
- `scripts/concise_prompt_experiment.py` 재사용 가능 여부 확인

## Steps

1. 직전 실험의 품질 리스크를 정리한다.
2. forced no-answer bullet을 제거/완화한 refined concise bullet prompt를 작성한다.
3. 대표 질의에서 baseline과 refined 후보를 비교한다.
4. 품질 리스크가 줄었는지 답변 preview와 trace latency를 함께 확인한다.
5. 채택 가능하면 사용자 승인 후 코드 반영, 서버 반영, 검증을 진행한다.

## Automated tests

- `.venv/bin/python -m py_compile retriever/engine.py retriever/llm.py query.py api/main.py app.py scripts/concise_prompt_experiment.py`
- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 또는 로컬 CLI/API 대표 질의 smoke
- trace `total`, `retrieval_total`, `llm`, `answer_length` 비교
- 답변이 근거를 유지하고 불필요한 "문서에서 확인되지 않습니다" 문장을 만들지 않는지 확인

## Skipped/Not Run

- full eval은 smoke에서 채택 가능성이 확인된 뒤 실행한다.
- 운영 배포는 사용자 승인 후 진행한다.

## Open Work

- refined concise bullet prompt 설계
- smoke 비교
