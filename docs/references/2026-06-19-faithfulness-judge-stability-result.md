# 2026-06-19 Faithfulness Judge Stability Result

## Summary

`tc-04`, `tc-23`에서 확인된 faithfulness judge 불안정성을 최소 변경으로 보정했다.

변경 내용:

- `eval/pipeline.py`의 faithfulness judge 호출에 `temperature=0.0`을 적용했다.
- faithfulness judge의 참고 문서 context에 source label을 포함했다.

최종 결과:

- `tc-04` focused smoke 통과
- `tc-23` 동일 answer/context 반복 판정 통과
- full eval 23개 케이스 전체 green
- source drift report 기준 critical/watch case 없음

## Changes

파일:

- `eval/pipeline.py`

변경 1:

```python
result = self._llm.predict(prompt, temperature=0.0)
```

이유:

- faithfulness judge는 평가용 binary 판정 경로다.
- 같은 answer/context에서 `YES/NO`가 흔들리면 품질 회귀와 평가기 흔들림을 구분하기 어렵다.
- answer generation과 달리 judge는 deterministic 설정이 적합하다.

변경 2:

```text
[출처: <source>]
<context chunk>
```

형태로 judge context에 source label을 포함했다.

이유:

- `tc-23` 답변은 `카카오`, `네이버`, `다음` 약관명을 언급했다.
- 기존 judge context는 chunk text만 제공하고 source label은 제외했다.
- 답변의 source label 언급은 실제 retrieved source에 근거하지만 judge prompt에서는 검증할 수 없어 `NO`가 안정적으로 발생했다.

## Focused Validation

`tc-04` after source-aware judge:

- 서버 report: `/opt/ragSystem_codex/eval/results/eval_tc04_source_aware_judge_20260619_100353.json`
- 결과: `answer_accuracy=1.0`, `faithfulness=1.0`, `source_recall_at_k=1.0`

`tc-23` same answer/context repeated judge:

```text
[1.0, 1.0, 1.0, 1.0, 1.0]
```

해석:

- source label 없는 deterministic judge에서는 `tc-23`이 반복적으로 `0.0`이었다.
- source label을 포함한 뒤 같은 answer/context 판정은 안정적으로 `1.0`이 됐다.

`tc-15` stochastic check:

- `eval_tc15_current_r1_20260619_101631.json`
- `eval_tc15_current_r2_20260619_101644.json`
- `eval_tc15_current_r3_20260619_101656.json`
- 3회 모두 `answer_accuracy=1.0`, `faithfulness=1.0`

## Full Eval

최종 full eval:

- 서버 report: `/opt/ragSystem_codex/eval/results/eval_20260619_102404.json`
- 로컬 report: `eval/results/eval_20260619_102404.json`
- Source drift report: `docs/references/2026-06-19-faithfulness-judge-stability-source-drift-report.md`

Metrics:

| Metric | Value |
| --- | ---: |
| `total_cases` | 23 |
| `accuracy_mean` | 1.0 |
| `faithfulness_mean` | 1.0 |
| `not_found_success_rate` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `rag_normalized_source_precision@k_mean` | 1.0 |
| `rag_chunk_precision@k_mean` | 0.8609 |

Source drift:

- critical case: 없음
- watch case: 없음

## Intermediate Results

중간 full eval:

- `eval/results/eval_20260619_095949.json`: `tc-23 faithfulness=0.0`
- `eval/results/eval_20260619_100940.json`: `tc-15 answer_accuracy=0.25`

판단:

- `tc-23`은 source label 미표시로 인한 judge 입력 문제였다.
- `tc-15`는 같은 기준에서 단일 반복 3회가 모두 통과해 answer generation stochastic 흔들림으로 분류했다.
- 최종 full eval 재실행에서는 전체 green을 확인했다.

## Latency Trace

최종 full eval 직후 서버의 최근 23개 `eval.case` trace 기준:

```text
count=23
first_timestamp=2026-06-19T01:19:50.844687+00:00
last_timestamp=2026-06-19T01:24:04.206453+00:00
mean_ms=9129.63
median_ms=8505.46
min_ms=2443.61
max_ms=19716.02
p95_ms=15505.34
```

## Decision

- `eval/pipeline.py`의 deterministic source-aware faithfulness judge 변경을 유지한다.
- `tc-04` answer wording prompt 변경은 채택하지 않는다.
- `tc-07`, `tc-15` eval rule calibration plan은 최종 full eval green 기준으로 완료 처리한다.
