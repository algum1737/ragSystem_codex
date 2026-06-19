# TC07 TC15 Eval Rule Calibration Plan

## Goal

`tc-07`, `tc-15`의 deterministic `answer_accuracy` keyword group을 실제 문서 근거와 동의 표현에 맞게 좁게 보정한다.

## Scope

- `eval/test_cases.json`의 `tc-07`, `tc-15` expected keyword OR group 보정
- 기존 eval report의 답변을 새 rule로 재점수
- full eval 재실행
- source drift report 재생성
- 결과 문서, `docs/index.md`, `docs/HANDOFF.md` 갱신

## Out Of Scope

- prompt 변경
- retrieval, reranker, chunking 변경
- model 변경
- eval scoring 함수 변경
- 운영 API/Web 배포

## Assumptions

- 최신 기준선은 `eval/results/eval_20260618_113500.json`이다.
- `tc-07`, `tc-15`는 retrieval/source/faithfulness 문제가 아니다.
- OR group 확장은 false positive를 피하기 위해 문서 의미가 분명한 좁은 표현만 추가한다.
- full eval에서 새 답변이 stochastic하게 달라질 수 있으므로 기존 report 재점수와 full eval을 둘 다 확인한다.

## Pre-flight checks

- [x] `git status --short --branch`
- [x] `bash scripts/validate-docs.sh`
- [x] 기존 실패 기준 확인
  - `tc-07 answer_accuracy=0.75`
  - `tc-15 answer_accuracy=0.75`
- [x] `docs/references/2026-06-18-tc07-tc15-focused-triage-result.md` 확인

## Steps

1. `eval/test_cases.json`의 `tc-07`, `tc-15` expected keyword를 보정한다.
2. 기존 report `eval/results/eval_20260618_113500.json`의 answer를 새 expected keyword로 재점수한다.
3. 서버에서 `gemma3:12b + top_k=5` full eval을 실행한다.
4. 새 eval report를 로컬로 복사한다.
5. 새 report로 source drift report를 생성한다.
6. 결과 문서를 작성한다.
7. plan을 completed로 이동하고 `docs/index.md`, `docs/HANDOFF.md`를 갱신한다.

## Task Breakdown

- [x] RED baseline
  - 명령:
    ```bash
    jq '.cases[] | select(.id=="tc-07" or .id=="tc-15") | {id, answer_accuracy}' eval/results/eval_20260618_113500.json
    ```
  - 기대 결과:
    - `tc-07=0.75`
    - `tc-15=0.75`
- [x] Rule calibration
  - 파일: `eval/test_cases.json`
  - 변경 후보:
    - `tc-07`: 첫 group을 `["면책", "책임을 부담하지", "책임을 지지", "책임이 없"]`로 확장
    - `tc-15`: 세 번째 group에 `"없이"`, `"예측할 수 없"`, `"통제할 수 없"` 추가
  - 제외:
    - `책임`, `경우`, `사유`, `가능`처럼 일반적이거나 반대 의미에도 나오는 표현
- [x] Existing report re-score
  - 명령:
    ```bash
    .venv/bin/python - <<'PY'
    import json
    # 기존 report answer를 수정된 eval/test_cases.json 기준으로 재점수
    PY
    ```
  - 기대 결과:
    - `tc-07=1.0`
    - `tc-15=1.0`
    - recalculated `accuracy_mean=1.0`
- [x] Full eval
  - 서버 명령:
    ```bash
    cd /opt/ragSystem_codex
    RAG_TRACE_ENABLED=true \
    RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
    CUDA_VISIBLE_DEVICES="" \
    .venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
    ```
  - 기대 결과:
    - 새 `eval/results/eval_*.json` 생성
    - `accuracy_mean=1.0`
    - `faithfulness_mean=1.0`
    - `not_found_success_rate=1.0`
- [x] Source drift report
  - 명령:
    ```bash
    .venv/bin/python scripts/source_drift_report.py eval/results/<new-report>.json \
      --test-cases eval/test_cases.json \
      --output docs/references/2026-06-18-tc07-tc15-eval-rule-calibration-source-drift-report.md
    ```
  - 기대 결과:
    - critical case 없음
    - watch case 없음 또는 기존 정책상 watch만 존재

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py scripts/source_drift_report.py`
- `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`
- `.venv/bin/python -m json.tool eval/test_cases.json >/dev/null`

## Manual/Runtime QA

- `tc-07`, `tc-15` 새 OR group이 실제 답변 의미와 일치하는지 확인한다.
- full eval 결과에서 회귀 케이스가 없는지 확인한다.
- 서버 health:
  - `systemctl is-active ragsystem-api ragsystem-web`
  - `curl -s http://127.0.0.1:8000/health`
  - `curl -s http://127.0.0.1:8501/_stcore/health`

## Skipped/Not Run

- prompt smoke는 실행하지 않는다. 이번 작업은 prompt 변경이 아니다.
- 운영 API/Web 배포는 실행하지 않는다. 평가셋 보정은 repo/eval 기준 변경이다.
- `concise` 실제 사용자 trace review는 별도 active plan에서 계속 추적한다.

## Open Work

- 없음.
- `tc-04` faithfulness blocker는 `docs/exec-plans/completed/2026-06-19-faithfulness-judge-stability.md`에서 해결했다.

## Completion

- 완료.
- `tc-07`, `tc-15` target calibration은 유지한다.
- 최초 full eval은 `tc-04 faithfulness=0.0` 때문에 green이 아니었지만, 후속 judge stability 변경 이후 최종 full eval 전체 기준을 충족했다.
- 결과 문서: `docs/references/2026-06-18-tc07-tc15-eval-rule-calibration-result.md`
- 최종 green 근거: `docs/references/2026-06-19-faithfulness-judge-stability-result.md`

## Validation Result

- 통과: `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: `.venv/bin/python -m json.tool eval/test_cases.json >/dev/null`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py scripts/source_drift_report.py`
- 통과: 기존 report 재점수
  - `tc-07=1.0`
  - `tc-15=1.0`
- 부분 통과: full eval
  - report: `eval/results/eval_20260618_132509.json`
  - `accuracy_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - `rag_normalized_source_precision@k_mean=1.0`
  - `tc-07 answer_accuracy=1.0`, `faithfulness=1.0`
  - `tc-15 answer_accuracy=1.0`, `faithfulness=1.0`
- 해결됨: full eval faithfulness
  - `faithfulness_mean=0.9565`
  - `tc-04 faithfulness=0.0`
  - `tc-04` 단일 재실행 report `/opt/ragSystem_codex/eval/results/eval_tc04_check_20260618_132648.json`에서도 `faithfulness=0.0`
- 통과: source drift report 생성
  - `docs/references/2026-06-18-tc07-tc15-eval-rule-calibration-source-drift-report.md`
  - critical case는 `tc-04`
- 통과: 후속 최종 full eval
  - report: `eval/results/eval_20260619_102404.json`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - `rag_normalized_source_precision@k_mean=1.0`
