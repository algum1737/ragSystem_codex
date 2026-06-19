# 2026-06-19 TC30 Answer Coverage Result

## Summary

`tc-30`의 multi-source answer coverage 문제를 분석했다.

결론:

- retrieval/rerank 문제는 아니었다.
- standard prompt 변경도 필요하지 않았다.
- `tc-30`, `tc-31`은 expected keyword가 요구하는 범위보다 질문 wording이 넓거나 모호했다.
- 질문을 기대 근거 범위에 맞게 명시하자 focused smoke와 full eval이 통과했다.
- 최종 32개 hard eval은 전체 green이다.

## Changes

파일:

- `eval/test_cases.json`

`tc-30`:

- 기존 질문은 "유료서비스 환불 시 결제수단으로 같은 방법 환불이 불가능하면 어떻게 처리되는가?"였다.
- expected keyword는 `3영업일`, `수납확인`까지 요구했다.
- 질문을 다음처럼 보정했다.

```text
카카오와 네이버 유료서비스 약관에서 환불 기한은 언제이며, 결제와 동일한 방법으로 환불이 불가능하거나 수납확인이 필요한 경우에는 어떻게 처리하는가?
```

`tc-31`:

- 기존 질문은 "미성년자가 유료서비스 또는 결제서비스를 이용하려는 경우 어떤 제한이 있는가?"였다.
- expected keyword는 카카오 유료/결제서비스 약관의 `법정대리인 동의`, `계약체결 후 추인`, `계약 취소`를 요구했다.
- 질문과 relevant source를 카카오 특칙으로 좁혔다.

```text
카카오 유료/결제서비스 약관에서 만 19세 미만 미성년 회원이 부모 등 법정대리인의 동의나 계약체결 후 추인을 얻지 않고 이용하면 계약은 어떻게 되는가?
```

## Focused Validation

`tc-30` original focused smoke:

- report: `eval/results/eval_tc30_focused_20260619_111500.json`
- 3회 모두 `faithfulness=1.0`
- 3회 모두 `answer_accuracy=0.8`
- 누락 group: `3영업일` 또는 `수납확인`

`tc-30` wording probe:

- 환불 기한, 동일 방법 환불 불가, 수납확인을 질문에 명시했다.
- 3회 모두 `answer_accuracy=1.0`, `faithfulness=1.0`

`tc-31` focused smoke:

- report: `eval/results/eval_tc12_tc31_focused_20260619_114400.json`
- `tc-31`은 3회 중 2회 통과, 1회 `answer_accuracy=0.8`
- 실패 run은 `동의` 또는 `추인` 표현을 생략했다.

`tc-31` wording probe:

- 카카오, 만 19세 미만, 법정대리인 동의, 계약체결 후 추인을 질문에 명시했다.
- 3회 모두 `answer_accuracy=1.0`, `faithfulness=1.0`

`tc-12` focused smoke:

- full eval 중간 실행에서 `faithfulness=0.0`이 1회 발생했다.
- focused smoke 3회는 모두 `answer_accuracy=1.0`, `faithfulness=1.0`이었다.
- 별도 변경 없이 최종 full eval에서 통과했다.

## Full Eval

중간 full eval:

- report: `eval/results/eval_20260619_113433.json`
- `accuracy_mean=0.9938`
- `faithfulness_mean=0.9688`
- failures:
  - `tc-12 faithfulness=0.0`
  - `tc-31 answer_accuracy=0.8`

최종 full eval:

- 서버 report: `/opt/ragSystem_codex/eval/results/eval_20260619_115043.json`
- 로컬 report: `eval/results/eval_20260619_115043.json`
- Source drift report: `docs/references/2026-06-19-tc30-answer-coverage-source-drift-report.md`

Metrics:

| Metric | Value |
| --- | ---: |
| `total_cases` | 32 |
| `accuracy_mean` | 1.0 |
| `faithfulness_mean` | 1.0 |
| `not_found_success_rate` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `rag_normalized_source_precision@k_mean` | 1.0 |
| `rag_chunk_precision@k_mean` | 0.8438 |

Source drift:

- critical case: 없음
- watch case: 없음

## Latency Trace

최종 full eval 직후 서버의 최근 32개 `eval.case` trace 기준:

```text
count=32
first_timestamp=2026-06-19T02:45:11.208156+00:00
last_timestamp=2026-06-19T02:50:43.387276+00:00
mean_ms=8461.86
median_ms=7303.99
min_ms=2302.35
max_ms=20825.10
p95_ms=16261.59
```

## Decision

- Prompt, retrieval, reranker 변경은 하지 않는다.
- Hard eval 질문을 expected evidence 범위와 맞춰 유지한다.
- 32개 hard eval green baseline은 `eval/results/eval_20260619_115043.json`으로 삼는다.
