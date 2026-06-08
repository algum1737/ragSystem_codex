# Post Transition Monitoring Plan

## Goal

`gemma3:12b + top_k=5` 운영 전환 후 실제 응답 속도와 안정성을 관찰하고 추가 튜닝 필요 여부를 결정한다.

## Scope

- 운영 API `/health`와 `/stats` 상태 재확인
- 최근 `api.query` trace latency 분포 확인
- `ollama ps` processor/GPU 상태 확인
- 추가 튜닝 후보 우선순위 결정

## Out Of Scope

- 모델 변경
- 프롬프트 변경
- `top_k` 변경
- systemd GPU 환경변수 변경

## Assumptions

- 현재 운영 기본 모델은 `gemma3:12b`다.
- 현재 운영 `top_k`는 5다.
- 전환 직후 대표 query는 약 22초, Ollama `100% GPU`로 확인됐다.

## Pre-flight checks

- `docs/references/2026-06-04-gemma3-operating-transition-result.md` 확인
- 서버 `/health` 모델 확인
- 최근 trace 파일 존재 확인

## Steps

1. 운영 상태와 최근 trace를 확인한다.
2. latency가 안정적인지 판단한다.
3. 필요 시 다음 후보를 `max_tokens`, API CPU 모드, `top_k=4` 중 하나로 좁힌다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 서버 `/health`, `/stats`, `ollama ps`, trace tail 확인

## Skipped/Not Run

- 모델 변경, 프롬프트 변경, `top_k` 변경, systemd GPU 환경변수 변경은 실행하지 않았다.
- full eval은 실행하지 않았다. 이번 작업은 전환 직후 운영 상태와 trace 관찰 범위다.

## Open Work

- 없음. 다음 active plan은 `docs/exec-plans/active/2026-06-04-gemma3-token-cap-experiment.md`다.

## Completion

- 전환 후 서버 `/health`, `/stats`, Streamlit HTTP 상태를 확인했다.
- 추가 대표 query 2건을 실행해 post-transition trace 표본을 보강했다.
- 최신 `api.query` trace에서 `gemma3:12b + top_k=5` latency를 확인했다.
- `ollama ps`에서 `gemma3:12b`가 `100% GPU`로 실행되는 것을 확인했다.
- 결론: 운영 전환은 정상이고, GPU 경합보다는 LLM 생성 길이/시간이 다음 병목이다.
- 다음 후보는 `gemma3:12b` 전용 `max_tokens` 제한 실험이다.
- 결과 문서: `docs/references/2026-06-04-post-transition-monitoring-result.md`

## Validation Result

- 통과: server health/status
  - `/health`: `{"status":"ok","model":"gemma3:12b"}`
  - `/stats`: `{"collection_name":"ragSystem","count":318}`
  - Streamlit: `HTTP/1.1 200 OK`
- 통과: server GPU/Ollama state
  - 추가 query 전 `ollama ps`: 상주 모델 없음
  - 추가 query 후 `ollama ps`: `gemma3:12b`, `100% GPU`, context 4096
  - idle GPU memory: GPU 0 약 6 MiB, GPU 1 약 15 MiB
- 통과: additional API query smoke
  - 위치기반서비스 query: elapsed 약 24.78초, answer length 426, source 5개
  - 운영정책 query: elapsed 약 7.72초, answer length 617, source 5개
- 통과: trace latency review
  - 전환 후 주요 3건: total 약 22.0초, 24.8초, 7.7초
  - LLM 구간이 여전히 주 병목
  - 위치기반서비스 추가 query는 embedding/rerank cold load 영향으로 retrieval 약 9.6초
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
