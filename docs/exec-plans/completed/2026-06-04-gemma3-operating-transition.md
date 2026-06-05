# Gemma3 Operating Transition Plan

## Goal

운영 응답 기본 모델을 `gemma3:12b + top_k=5`로 전환할지 승인받고, 승인 시 코드/운영 설정/문서를 일관되게 반영한다.

## Scope

- 현재 운영 API 모델(`gemma4:e4b`)과 코드 기본값(`gemma4:26b`) 불일치 정리
- `gemma3:12b + top_k=5` 운영 전환 방식 결정
- 승인 시 API 기본 모델, CLI 기본 모델, 문서의 운영 모델 표기 갱신
- 승인 시 서버 런타임 모델 변경 또는 재배포 반영
- 전환 후 `/health`, 대표 `/query`, trace latency 확인

## Out Of Scope

- `top_k=4` full eval
- API embedding/reranker CPU 모드 systemd 변경
- GPU/driver 변경
- 프롬프트 또는 평가셋 변경
- `gemma4:e4b` full eval

## Assumptions

- `gemma3:12b + top_k=5`는 현재 가장 균형 잡힌 속도/품질 후보이다.
- 운영 전환은 사용자의 명시 승인이 필요하다.
- `top_k=5`는 현재 코드 기본값이므로 모델만 전환해도 source recall 회귀를 피할 수 있다.

## Pre-flight checks

- 사용자에게 운영 모델 전환 승인 확인
- `git status --short` 확인
- 서버 `/health` 현재 모델 확인
- 서버 `gemma3:12b` availability 확인
- 기준선 `eval/results/eval_20260602_131307.json` 확인

## Steps

1. 전환 승인과 범위를 확정한다.
2. 코드 기본 모델과 사용자-facing 문서의 운영 모델 표기를 `gemma3:12b`로 갱신한다.
3. 서버 API 런타임 모델을 `gemma3:12b`로 전환하거나 재배포 절차를 수행한다.
4. `/health`와 대표 `/query` trace latency를 확인한다.
5. 완료 범위와 검증 결과를 문서에 남긴다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile retriever/llm.py query.py api/main.py app.py`

## Manual/Runtime QA

- 서버 `/health`가 `gemma3:12b`를 반환하는지 확인
- 대표 `/query`가 정상 답변을 반환하고 trace가 기록되는지 확인
- `ollama ps`에서 모델 processor 상태 확인

## Skipped/Not Run

- `top_k=4` full eval은 실행하지 않았다. `top_k=5` 기준선이 가장 안정적인 운영 후보였기 때문이다.
- API embedding/reranker CPU 모드 systemd 변경은 실행하지 않았다. 모델 전환만으로 우선 latency 개선을 확인했다.
- `gemma4:e4b` full eval은 실행하지 않았다. 현재 전환 후보가 `gemma3:12b + top_k=5`로 결정됐기 때문이다.

## Open Work

- 없음. 다음 active plan은 `docs/exec-plans/active/2026-06-04-post-transition-monitoring.md`다.

## Completion

- 사용자 승인 후 운영 응답 기본 모델을 `gemma3:12b`로 전환했다.
- `top_k`는 기존 기본값 5를 유지했다.
- 코드 기본 모델과 CLI 기본 모델을 `gemma3:12b`로 갱신했다.
- Streamlit 추천 모델 목록에서 `gemma3:12b`를 운영 기본값으로 표시하고 `gemma4:26b`를 품질 우선 모델로 낮췄다.
- 아키텍처 문서, 배포 가이드, 서버 기동 가이드의 현재 운영 기본 모델 표기를 `gemma3:12b`로 갱신했다.
- 변경 파일을 Ubuntu 서버 `/opt/ragSystem_codex`에 반영했다.
- 서버 API 런타임 모델을 `/model` endpoint로 `gemma4:e4b`에서 `gemma3:12b`로 전환했다.
- API 프로세스를 재시작해 코드 기본값으로도 `/health`가 `gemma3:12b`를 반환하는지 확인했다.
- Streamlit 프로세스도 재시작해 새 `app.py`를 반영했다.
- 결과 문서: `docs/references/2026-06-04-gemma3-operating-transition-result.md`

## Validation Result

- 통과: 사용자 승인
  - 요청: "진행하자"
- 통과: 로컬 compile
  - `.venv/bin/python -m py_compile retriever/llm.py query.py api/main.py app.py`
- 통과: 로컬 문서 검증
  - `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: 서버 compile
  - `.venv/bin/python -m py_compile retriever/llm.py query.py api/main.py app.py`
  - 서버 `retriever.llm.DEFAULT_MODEL`: `gemma3:12b`
- 통과: 서버 runtime model change
  - before `/health`: `{"status":"ok","model":"gemma4:e4b"}`
  - `PUT /model {"model":"gemma3:12b"}`: previous `gemma4:e4b`
  - after `/health`: `{"status":"ok","model":"gemma3:12b"}`
- 통과: representative API query smoke
  - question: `서비스 해지 시 데이터 및 게시물은 어떻게 처리되는가?`
  - status: 200
  - elapsed: 약 22.05초
  - answer length: 998
  - trace: `model=gemma3:12b`, `top_k=5`, `total=22045.29ms`, `llm=21908.49ms`
  - `ollama ps`: `gemma3:12b`, `100% GPU`, context 4096
- 통과: API restart persistence
  - API 프로세스 재시작 후 `/health`: `{"status":"ok","model":"gemma3:12b"}`
  - `/stats`: `{"collection_name":"ragSystem","count":318}`
- 통과: Streamlit restart
  - 재시작 후 `HTTP/1.1 200 OK`
