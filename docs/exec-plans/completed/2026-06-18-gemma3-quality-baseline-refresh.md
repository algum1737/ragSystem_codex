# Gemma3 Quality Baseline Refresh Plan

## Goal

현재 운영 기준인 `gemma3:12b + top_k=5`의 품질 기준선을 다시 측정하고, 남은 품질 개선 후보를 `retrieval/source`, `prompt/answer`, `eval rule`, `model/runtime` 문제로 분류한다.

## Scope

- 최신 full eval 기준선 재측정
- source drift report 생성 및 critical/watch case 확인
- answer accuracy, faithfulness, not-found, source recall, latency 지표 비교
- 실패 또는 약점 케이스를 원인별로 분류
- 다음 개선 후보 1개를 후속 active plan 후보로 정리

## Out Of Scope

- 운영 모델 변경
- `PROMPT_TEMPLATE` 또는 `CONCISE_PROMPT_TEMPLATE` 변경
- 평가셋/판정 rule 변경
- 검색 알고리즘, reranker, chunking 변경
- 서버 배포 또는 systemd 설정 변경

## Assumptions

- 현재 운영 품질 기준은 `gemma3:12b + top_k=5`다.
- 품질 개선은 full eval과 source drift report를 먼저 보고 결정한다.
- 이전 `top_k=3` 실험은 latency는 개선했지만 source recall 회귀로 채택하지 않았다.
- 실제 품질 문제와 eval rule 문제를 분리하지 않은 상태에서 prompt를 바꾸지 않는다.
- 구현 변경이 필요한 개선은 별도 사용자 승인 후 진행한다.

## Pre-flight checks

- [x] `git status --short --branch`
- [x] `bash scripts/validate-docs.sh`
- [x] `.venv/bin/python eval/pipeline.py --help`
- [x] 서버 API/Web health 확인
- [x] 운영 서버의 현재 model과 Chroma count 확인
- [x] 기존 기준선 리포트 확인
  - `eval/results/eval_20260601_164832.json`
  - `eval/results/eval_20260602_131307.json`
  - `eval/results/eval_20260604_171559.json`

## Steps

1. 현재 repo와 서버 상태를 확인한다.
2. `gemma3:12b + top_k=5` full eval을 실행해 최신 기준선을 만든다.
3. 새 eval 리포트로 source drift report를 생성한다.
4. 최신 기준선을 이전 기준선과 비교한다.
5. 실패/약점 케이스를 원인별로 분류한다.
6. latency trace를 함께 확인해 품질 개선 후보가 성능 회귀를 만들 가능성을 기록한다.
7. 결과 문서를 `docs/references/`에 작성한다.
8. 다음 개선 후보를 1개만 선정하고, 구현이 필요하면 별도 active plan 또는 사용자 승인 지점으로 남긴다.

## Task Breakdown

- [x] Baseline run
  - 서버 명령:
    ```bash
    cd /opt/ragSystem_codex
    RAG_TRACE_ENABLED=true \
    RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
    CUDA_VISIBLE_DEVICES="" \
    .venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
    ```
  - 기대 결과:
    - `eval/results/eval_*.json` 새 리포트 생성
    - summary에 `accuracy_mean`, `faithfulness_mean`, `not_found_success_rate`, `source_recall@k_mean`, `rag_normalized_source_precision@k_mean` 포함
- [x] Source drift report
  - 로컬 또는 서버 명령:
    ```bash
    .venv/bin/python scripts/source_drift_report.py eval/results/<new-report>.json \
      --test-cases eval/test_cases.json \
      --output docs/references/2026-06-18-gemma3-quality-baseline-source-drift-report.md
    ```
  - 기대 결과:
    - critical/watch case가 표로 정리됨
    - critical이 있으면 원인 분류 대상으로 삼고, 즉시 code fix로 넘어가지 않음
- [x] Baseline comparison
  - 비교 기준:
    - `eval/results/eval_20260602_131307.json`: `gemma3:12b + top_k=5` 이전 기준선
    - `eval/results/eval_20260604_171559.json`: `gemma3:12b + top_k=3` rejected 기준선
  - 기대 결과:
    - metric 유지/회귀/개선 여부가 표로 정리됨
- [x] Failure triage
  - 분류 기준:
    - `retrieval/source`: relevant source 누락, source recall/precision 문제
    - `prompt/answer`: 근거는 있으나 답변 구성, 불필요한 섹션, source 혼합 문제
    - `eval rule`: 실제 답변은 유효하지만 keyword 또는 deterministic rule이 좁은 문제
    - `model/runtime`: stochastic output, latency, timeout, model loading 문제
  - 기대 결과:
    - 다음 실험 후보가 1개로 좁혀짐
- [x] Result docs
  - 작성 경로:
    - `docs/references/2026-06-18-gemma3-quality-baseline-refresh-result.md`
  - 기대 결과:
    - 실행 환경, 명령, 리포트 경로, 지표, 원인 분류, 다음 후보 포함

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py scripts/source_drift_report.py`
- `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`

## Manual/Runtime QA

- 서버 health:
  - `systemctl is-active ragsystem-api ragsystem-web`
  - `curl -s http://127.0.0.1:8000/health`
  - `curl -s http://127.0.0.1:8501/_stcore/health`
- 서버 stats:
  - `curl -s http://127.0.0.1:8000/stats`
- latency trace:
  - 새 eval run의 `eval.case` trace count, mean/median/p95 `query_total` 확인
- 실패 케이스 QA:
  - failed/watch case의 answer, retrieved sources, expected fields를 사람이 비교

## Skipped/Not Run

- 운영 모델 변경은 실행하지 않는다.
- prompt, eval rule, retrieval code 변경은 실행하지 않는다.
- full eval 결과가 불안정하면 동일 조건 재실행은 별도 판단으로 남긴다.
- `concise` 실제 사용자 trace review는 별도 active plan에서 계속 추적한다.

## Open Work

- 후속 후보는 `tc-07`, `tc-15` focused triage다.
- 구현 변경이 필요하면 사용자 승인 후 별도 RED-GREEN-REFACTOR 계획으로 진행한다.

## Completion

- 완료.
- `gemma3:12b + top_k=5` full eval을 재실행했다.
- 결과 문서는 `docs/references/2026-06-18-gemma3-quality-baseline-refresh-result.md`다.
- source drift report는 `docs/references/2026-06-18-gemma3-quality-baseline-source-drift-report.md`다.
- 최신 eval report는 `eval/results/eval_20260618_113500.json`이다.
- 다음 개선 후보는 `tc-07`, `tc-15`의 answer wording과 eval rule 정합성 triage다.

## Validation Result

- 통과: `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: `.venv/bin/python eval/pipeline.py --help`
  - full eval, concise lightweight, model, top-k 옵션 확인.
- 통과: 서버 health
  - `ragsystem-api: active`
  - `ragsystem-web: active`
  - API `/health`: `{"status":"ok","model":"gemma3:12b"}`
  - API `/stats`: `{"collection_name":"ragSystem","count":318}`
  - Streamlit health: `ok`
- 통과: full eval
  - report: `eval/results/eval_20260618_113500.json`
  - `accuracy_mean=0.9783`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - `rag_normalized_source_precision@k_mean=1.0`
- 통과: source drift report
  - critical: `tc-07`, `tc-15`
  - watch: 없음
  - 두 critical case 모두 source recall과 RAG precision은 `1.0`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py scripts/source_drift_report.py`
- 통과: `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`
  - `concise eval case schema valid: 6 cases`
