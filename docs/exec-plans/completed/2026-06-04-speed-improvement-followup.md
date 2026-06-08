# Speed Improvement Follow-Up Plan

## Goal

`gemma3:12b + top_k=3` full eval 회귀 이후, 답변 속도를 개선하기 위한 다음 운영 후보를 결정한다.

## Scope

- `gemma3:12b + top_k=5` 운영 후보 재검토
- `top_k=4` 중간 실험 필요 여부 판단
- API embedding/reranker CPU 모드로 GPU 경합을 줄이는 실험 필요 여부 판단
- 현재 운영 API 모델 상태(`gemma4:e4b`)와 문서상 운영 기본 모델(`gemma4:26b`) 차이 정리

## Out Of Scope

- 운영 모델 즉시 변경
- systemd 서비스 설정 변경
- GPU/driver 변경
- 평가셋 keyword 또는 prompt 변경

## Assumptions

- `gemma3:12b + top_k=3`은 latency는 좋지만 source recall과 accuracy가 회귀해 채택하지 않는다.
- `gemma3:12b + top_k=5`는 기존 full eval에서 `accuracy_mean=0.9891`, `faithfulness_mean=0.9565`, `not_found_success_rate=1.0`을 기록했다.
- 답변 속도 병목은 주로 LLM 생성 구간이며 retrieval은 상대적으로 작은 비중이다.

## Pre-flight checks

- 현재 서버 API `/health` 모델 확인
- 최신 completed plan `docs/exec-plans/completed/2026-06-02-gemma3-topk3-full-eval.md` 확인
- 최신 결과 문서 `docs/references/2026-06-04-gemma3-topk3-full-eval-result.md` 확인

## Steps

1. `gemma3:12b + top_k=5`, `gemma3:12b + top_k=3`, `gemma4:e4b`, `gemma4:26b`의 기존 latency/quality 근거를 표로 정리한다.
2. 운영 후보를 `gemma3:12b + top_k=5`, `top_k=4` 실험, API CPU 모드 실험으로 나누어 비용과 리스크를 비교한다.
3. 다음 실행 plan을 하나로 좁힌다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 필요 시 서버 `/health`, trace tail, `ollama ps`, `nvidia-smi`를 읽기 전용으로 확인한다.

## Skipped/Not Run

- 후속 실험은 실행하지 않았다. 이번 작업은 기존 trace/eval 근거를 비교해 다음 운영 후보를 결정하는 범위다.

## Open Work

- 없음. 다음 실행 plan은 `docs/exec-plans/active/2026-06-04-gemma3-operating-transition.md`다.

## Completion

- 현재 서버 API `/health`가 `model=gemma4:e4b`임을 확인했다.
- `ollama ps`는 비어 있어 상주 LLM 모델은 없었다.
- GPU 0은 API Python 프로세스가 약 3.5GB를 점유 중인 상태였다.
- 기존 trace/eval 근거를 비교해 다음 운영 후보를 `gemma3:12b + top_k=5`로 좁혔다.
- `top_k=4` 실험은 보조 후보로 남기되, 이미 품질 기준선이 있는 `top_k=5` 전환 판단을 우선한다.
- API embedding/reranker CPU 모드 실험은 `gemma4` 계열을 유지할 경우의 보조 후보로 남긴다.
- 결과 문서: `docs/references/2026-06-04-speed-improvement-followup-result.md`

## Validation Result

- 통과: 서버 현재 상태 확인
  - `/health`: `{"status":"ok","model":"gemma4:e4b"}`
  - `ollama ps`: 상주 모델 없음
  - GPU 0: 약 3562 MiB 사용, GPU util 0%
- 통과: 기존 기준선 비교
  - `gemma3:12b + top_k=5`: `accuracy_mean=0.9891`, `faithfulness_mean=0.9565`, `source_recall@k_mean=1.0`
  - `gemma3:12b + top_k=3`: `accuracy_mean=0.942`, `faithfulness_mean=0.9565`, `source_recall@k_mean=0.8449`
  - API trace 평균: `gemma3:12b + top_k=5` 약 23.8초, `gemma4:e4b + top_k=5` 약 26.1초, `gemma4:26b + top_k=5` 약 221.4초
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
