# 2026-06-19 TC04 Answer Wording Fix Result

## Summary

`tc-04`의 answer wording focused fix를 시도했지만 최종 변경으로 채택하지 않았다.

결론:

- `retriever/engine.py` standard prompt 보강은 단일 smoke에서는 통과했지만 반복 smoke와 full eval에서 안정적이지 않았다.
- prompt 변경은 되돌렸다.
- 최종 green 회복은 별도 `faithfulness judge` 안정화 변경으로 달성했다.
- `tc-04`는 최종 검증에서 `answer_accuracy=1.0`, `faithfulness=1.0`, `source_recall_at_k=1.0`이다.

## Attempted Change

대상 파일:

- `retriever/engine.py`

시도한 방향:

- 질문이 명시적으로 하위 항목, 비교 대상, 확인/미확인 항목을 요구하지 않으면 `문서에서 확인되지 않는 내용` 섹션을 만들지 않도록 standard prompt를 좁게 보강했다.
- 확인된 자동 갱신/정기결제/만료/고지/중단 조건 중심으로 답하게 했다.

채택하지 않은 이유:

- focused smoke 1회는 통과했다.
- 그러나 `tc-04` 반복 smoke에서 `faithfulness=0.0`이 다시 발생했다.
- full eval도 `tc-04 faithfulness=0.0`으로 실패했다.
- 원인은 answer wording 하나가 아니라 binary faithfulness judge의 stochastic 판정과 source label 미표시 문제까지 포함했다.

## Validation During Attempt

Prompt 보강 후 focused smoke:

- 서버 report: `/opt/ragSystem_codex/eval/results/eval_tc04_wording_fix_20260619_093201.json`
- 결과: `answer_accuracy=1.0`, `faithfulness=1.0`, `source_recall_at_k=1.0`

Prompt 보강 후 full eval:

- 서버 report: `/opt/ragSystem_codex/eval/results/eval_20260619_093659.json`
- 로컬 report: `eval/results/eval_20260619_093659.json`
- 결과: `accuracy_mean=1.0`, `faithfulness_mean=0.9565`
- 실패: `tc-04 faithfulness=0.0`

Prompt 보강 후 `tc-04` 반복 smoke:

- `eval_tc04_wording_fix_r1_20260619_093919.json`: `faithfulness=0.0`
- `eval_tc04_wording_fix_r2_20260619_093935.json`: `faithfulness=1.0`
- `eval_tc04_wording_fix_r3_20260619_093952.json`: `faithfulness=1.0`

추가 prompt 강화 후 full eval:

- 서버 report: `/opt/ragSystem_codex/eval/results/eval_20260619_095038.json`
- 로컬 report: `eval/results/eval_20260619_095038.json`
- 결과: `accuracy_mean=0.9457`, `faithfulness_mean=0.9565`
- 실패: `tc-12`, `tc-16`
- 판단: `tc-04`를 겨냥한 prompt 강화가 다른 케이스 회귀를 만들 수 있어 채택하지 않는다.

## Final Resolution

최종 변경은 `docs/references/2026-06-19-faithfulness-judge-stability-result.md`에 기록했다.

핵심 변경:

- `eval/pipeline.py`의 faithfulness judge 호출을 `temperature=0.0`으로 고정했다.
- faithfulness judge context에 source label을 포함했다.

최종 full eval:

- 서버 report: `/opt/ragSystem_codex/eval/results/eval_20260619_102404.json`
- 로컬 report: `eval/results/eval_20260619_102404.json`

| Metric | Value |
| --- | ---: |
| `accuracy_mean` | 1.0 |
| `faithfulness_mean` | 1.0 |
| `not_found_success_rate` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `rag_normalized_source_precision@k_mean` | 1.0 |

## Decision

- `retriever/engine.py` prompt 변경은 채택하지 않는다.
- `tc-04` plan은 별도 judge stability plan으로 superseded 처리한다.
- 후속으로는 prompt가 아니라 평가기 안정성 변경을 유지한다.
