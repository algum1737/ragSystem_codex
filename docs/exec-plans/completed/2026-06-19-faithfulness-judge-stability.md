# Faithfulness Judge Stability Plan

## Goal

`tc-04`처럼 동일한 faithful answer도 `YES/NO`가 흔들리는 faithfulness judge를 최소 변경으로 안정화한다.

## Scope

- `eval/pipeline.py`의 faithfulness judge LLM 호출 안정화
- `tc-04` focused smoke 반복
- full eval 재실행
- source drift report 재생성
- 결과 문서화

## Out Of Scope

- answer generation prompt 추가 변경
- `eval/test_cases.json` 추가 변경
- retrieval, reranker, chunking 변경
- operating model 변경
- 운영 API/Web 배포

## Assumptions

- `tc-04` focused smoke에서 positive grounded answer도 judge가 1회 `NO`로 판정했다.
- 실패 답변 자체의 source coverage는 충분하다.
- Faithfulness judge는 평가용 판정 경로이므로 answer generation보다 더 낮은 randomness가 필요하다.

## Pre-flight checks

- [ ] `git status --short --branch`
- [ ] `bash scripts/validate-docs.sh`
- [ ] `tc-04` focused smoke 반복 결과 확인
  - run1 `faithfulness=0.0`
  - run2 `faithfulness=1.0`
  - run3 `faithfulness=1.0`

## Steps

1. `eval/pipeline.py`의 `faithfulness()`에서 judge LLM 호출을 deterministic 설정으로 바꾼다.
2. 서버에 변경 파일을 반영한다.
3. `tc-04` focused smoke를 반복 실행한다.
4. full eval을 실행한다.
5. source drift report를 생성한다.
6. 결과 문서와 handoff를 갱신한다.

## Task Breakdown

- [ ] Judge call change
  - 파일: `eval/pipeline.py`
  - 변경:
    ```python
    result = self._llm.predict(prompt, temperature=0.0)
    ```
  - 기대 결과:
    - faithfulness judge 출력 흔들림 감소
- [ ] Focused smoke
  - 서버에서 `tc-04` 단일 케이스 3회 반복
  - 기대 결과:
    - 3회 모두 `answer_accuracy=1.0`
    - 3회 모두 `faithfulness=1.0`
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

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py`
- `.venv/bin/python -m json.tool eval/test_cases.json >/dev/null`
- `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`

## Manual/Runtime QA

- `tc-04` repeated focused smoke 결과 확인
- full eval critical/watch case 확인
- source drift report 확인

## Skipped/Not Run

- 운영 API/Web restart는 실행하지 않는다.
- concise mode smoke는 실행하지 않는다.

## Open Work

- deterministic judge 호출만으로도 회귀가 남으면 faithfulness prompt 자체를 별도 plan에서 검토한다.

## Completion

- 완료.
- `eval/pipeline.py`의 faithfulness judge를 deterministic source-aware 판정으로 보정했다.
- `tc-04`, `tc-23` focused 확인과 최종 full eval green을 확인했다.
- 결과 문서: `docs/references/2026-06-19-faithfulness-judge-stability-result.md`
- Source drift report: `docs/references/2026-06-19-faithfulness-judge-stability-source-drift-report.md`

## Validation Result

- 통과: pre-flight `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: pre-flight `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: deterministic judge 후 `tc-04` focused smoke 3회
  - `eval_tc04_judge_only_r1_20260619_095316.json`
  - `eval_tc04_judge_only_r2_20260619_095331.json`
  - `eval_tc04_judge_only_r3_20260619_095344.json`
  - 3회 모두 `answer_accuracy=1.0`, `faithfulness=1.0`
- 실패 확인: deterministic judge만 적용한 full eval
  - report: `eval/results/eval_20260619_095949.json`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=0.9565`
  - 실패: `tc-23 faithfulness=0.0`
- 원인 확인: `tc-23` same answer/context 반복 판정
  - source label 없는 context: `[0.0, 0.0, 0.0, 0.0, 0.0]`
  - source-aware context 적용 후: `[1.0, 1.0, 1.0, 1.0, 1.0]`
- 통과: source-aware judge 후 `tc-04` focused smoke
  - report: `/opt/ragSystem_codex/eval/results/eval_tc04_source_aware_judge_20260619_100353.json`
  - `answer_accuracy=1.0`
  - `faithfulness=1.0`
  - `source_recall_at_k=1.0`
- 중간 실패: source-aware judge 후 첫 full eval
  - report: `eval/results/eval_20260619_100940.json`
  - `accuracy_mean=0.9674`
  - `faithfulness_mean=1.0`
  - 실패: `tc-15 answer_accuracy=0.25`
- 통과: `tc-15` 단일 3회 재확인
  - `eval_tc15_current_r1_20260619_101631.json`
  - `eval_tc15_current_r2_20260619_101644.json`
  - `eval_tc15_current_r3_20260619_101656.json`
  - 3회 모두 `answer_accuracy=1.0`, `faithfulness=1.0`
- 통과: 최종 full eval
  - report: `eval/results/eval_20260619_102404.json`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `source_recall@k_mean=1.0`
  - `rag_normalized_source_precision@k_mean=1.0`
- 통과: source drift report
  - critical case: 없음
  - watch case: 없음
- 통과: 최종 full eval latency trace 확인
  - `count=23`
  - `mean_ms=9129.63`
  - `median_ms=8505.46`
  - `p95_ms=15505.34`
