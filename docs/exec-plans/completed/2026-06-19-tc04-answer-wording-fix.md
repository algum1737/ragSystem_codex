# TC04 Answer Wording Fix Plan

## Goal

`tc-04` 자동 갱신 케이스에서 faithful한 positive answer가 생성되도록 standard answer prompt를 좁게 보강한다.

## Scope

- `retriever/engine.py`의 `PROMPT_TEMPLATE` 최소 수정
- `tc-04` focused smoke
- full eval 재실행
- source drift report 재생성
- `tc-07`, `tc-15` eval rule calibration active plan 완료 여부 판단
- 결과 문서, `docs/index.md`, `docs/HANDOFF.md` 갱신

## Out Of Scope

- `CONCISE_PROMPT_TEMPLATE` 변경
- retrieval, reranker, chunking 변경
- model 변경
- faithfulness judge 변경
- `eval/test_cases.json` 추가 변경
- 운영 API/Web systemd 설정 변경

## Assumptions

- `tc-04` failure의 primary cause는 answer wording이다.
- 명시적 하위 항목이 아닌 질문에서 `문서에서 확인되지 않는 내용` 섹션을 만들지 않도록 하면 positive-only answer에 가까워질 수 있다.
- 답변 전체를 짧게 만드는 것이 아니라, 확인된 근거 중심으로 답하고 불필요한 negative section을 줄이는 것이 목표다.

## Pre-flight checks

- [ ] `git status --short --branch`
- [ ] `bash scripts/validate-docs.sh`
- [ ] `docs/references/2026-06-18-tc04-faithfulness-triage-result.md` 확인
- [ ] RED 기준 확인
  - `eval/results/eval_20260618_132509.json`에서 `tc-04 faithfulness=0.0`

## Steps

1. Standard prompt에 "명시적 하위 항목이 아닌 질문" 처리 규칙을 추가한다.
2. 로컬 정적 검증을 실행한다.
3. 변경된 `retriever/engine.py`를 서버에 반영한다.
4. 서버에서 `tc-04` 단일 focused smoke를 실행한다.
5. focused smoke가 통과하면 full eval을 실행한다.
6. full eval report를 로컬로 복사한다.
7. source drift report를 생성한다.
8. 결과 문서와 handoff를 갱신한다.

## Task Breakdown

- [ ] Prompt change
  - 파일: `retriever/engine.py`
  - 변경 방향:
    - 기존 rule 3의 하위 항목 처리 아래에 제한 문구 추가
    - 명시적으로 여러 하위 항목, 비교 대상, 확인/미확인 항목을 물은 경우에만 `문서에서 확인되지 않는 내용` 섹션을 사용
    - 그 외에는 확인된 내용 중심으로 답하고, 불필요한 미확인 섹션을 만들지 않음
- [ ] Focused smoke
  - 서버 명령:
    ```bash
    cd /opt/ragSystem_codex
    RAG_TRACE_ENABLED=true \
    RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
    CUDA_VISIBLE_DEVICES="" \
    .venv/bin/python - <<'PY'
    # tc-04 single-case eval
    PY
    ```
  - 기대 결과:
    - `tc-04 answer_accuracy=1.0`
    - `tc-04 faithfulness=1.0`
    - `source_recall_at_k=1.0`
- [ ] Full eval
  - 서버 명령:
    ```bash
    cd /opt/ragSystem_codex
    RAG_TRACE_ENABLED=true \
    RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
    CUDA_VISIBLE_DEVICES="" \
    .venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
    ```
  - 기대 결과:
    - `accuracy_mean=1.0`
    - `faithfulness_mean=1.0`
    - `not_found_success_rate=1.0`
    - `source_recall@k_mean=1.0`
    - `tc-07`, `tc-15` 유지
- [ ] Source drift report
  - 명령:
    ```bash
    .venv/bin/python scripts/source_drift_report.py eval/results/<new-report>.json \
      --test-cases eval/test_cases.json \
      --output docs/references/2026-06-19-tc04-answer-wording-fix-source-drift-report.md
    ```

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile retriever/engine.py eval/pipeline.py scripts/source_drift_report.py`
- `.venv/bin/python -m json.tool eval/test_cases.json >/dev/null`
- `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`

## Manual/Runtime QA

- `tc-04` answer가 positive grounded content 중심인지 확인한다.
- `문서에서 확인되지 않는 내용` 섹션이 불필요하게 생성되지 않는지 확인한다.
- full eval의 critical/watch case를 source drift report로 확인한다.

## Skipped/Not Run

- concise mode smoke는 실행하지 않는다. concise prompt는 변경하지 않는다.
- 운영 API/Web restart는 실행하지 않는다. eval 서버 코드 반영만 수행한다.

## Open Work

- full eval에서 다른 케이스가 회귀하면 systematic debugging으로 원인을 분류한다.

## Completion

- 완료.
- 이 plan의 prompt wording 변경은 최종 채택하지 않았다.
- `retriever/engine.py` 변경은 되돌렸고, 최종 코드 변경은 없다.
- `tc-04` green 회복은 `docs/exec-plans/completed/2026-06-19-faithfulness-judge-stability.md`의 deterministic source-aware judge 변경으로 달성했다.
- 결과 문서: `docs/references/2026-06-19-tc04-answer-wording-fix-result.md`

## Validation Result

- 통과: pre-flight `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: pre-flight `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: 로컬 정적 검증
  - `.venv/bin/python -m py_compile retriever/engine.py eval/pipeline.py`
- 부분 통과: prompt wording 변경 후 `tc-04` focused smoke 1회
  - report: `/opt/ragSystem_codex/eval/results/eval_tc04_wording_fix_20260619_093201.json`
  - `answer_accuracy=1.0`
  - `faithfulness=1.0`
  - `source_recall_at_k=1.0`
- 실패: prompt wording 변경 후 full eval
  - report: `eval/results/eval_20260619_093659.json`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=0.9565`
  - 실패: `tc-04 faithfulness=0.0`
- 실패/불안정: prompt wording 변경 후 `tc-04` 반복 smoke
  - `eval_tc04_wording_fix_r1_20260619_093919.json`: `faithfulness=0.0`
  - `eval_tc04_wording_fix_r2_20260619_093935.json`: `faithfulness=1.0`
  - `eval_tc04_wording_fix_r3_20260619_093952.json`: `faithfulness=1.0`
- 통과: final resolution
  - `retriever/engine.py` prompt 변경 되돌림.
  - `eval/pipeline.py` judge stability 변경 후 최종 full eval green.
  - 최종 report: `eval/results/eval_20260619_102404.json`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - `rag_normalized_source_precision@k_mean=1.0`
