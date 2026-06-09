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

- 없음. v4는 full eval 회귀로 운영 기본 프롬프트 채택을 보류하고 기존 기본 프롬프트로 원복했다.

## Progress

- `scripts/concise_prompt_experiment.py`에 `refined_concise_bullet` 후보를 추가했다.
- 기존 `concise_bullet`의 forced no-answer 규칙은 제거했다.
- 출처 표기는 `출처:` 뒤 실제 문서명을 쓰도록 보강했다.
- 답변은 3~4개 bullet, 유사 조건 병합, 근거 최대 3개로 압축했다.
- 서버 smoke는 v1-v4까지 반복했고 최종 후보는 v4로 정했다.
- 결과 문서는 `docs/references/2026-06-09-refined-concise-bullet-prompt-result.md`에 기록했다.
- v4를 `retriever/engine.py` 기본 프롬프트에 임시 반영하고 서버 API smoke를 실행했다.
- 임시 반영 후 full eval에서 `accuracy_mean=0.8804`, `not_found_success_rate=0.0` 회귀를 확인했다.
- full eval 실패 후 로컬과 서버의 기본 프롬프트를 기존 버전으로 원복했다.

## Interim Validation Result

- 통과: `.venv/bin/python -m py_compile scripts/concise_prompt_experiment.py`
- 통과: 서버 v3 full comparison smoke
- 통과: 서버 v4 refined-only smoke
- 통과: v4 평균 total 5116.24ms, LLM 5008.91ms, answer length 298.0
- 통과: 운영 기본 프롬프트 임시 반영 후 API smoke
  - 위치기반서비스 warmed API smoke: total 5895.78ms, LLM 5770.59ms, answer length 331
  - 운영정책 warmed API smoke: total 4545.44ms, LLM 4432.80ms, answer length 251
- 실패: 운영 기본 프롬프트 임시 반영 후 full eval
  - 리포트: `/opt/ragSystem_codex/eval/results/eval_20260609_095553.json`
  - `accuracy_mean=0.8804`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=0.0`
- 통과: full eval 실패 후 로컬/서버 기본 프롬프트 원복

## Completion

- refined concise bullet 후보는 속도 개선 효과를 보였지만 full eval 품질 기준을 만족하지 못했다.
- 운영 기본 프롬프트로 채택하지 않는다.
- 다음 작업은 기본 프롬프트 교체가 아니라 선택형 concise answer mode 또는 no-answer 안전 라우팅 설계로 진행한다.
