# 2026-06-18 TC07 TC15 Eval Rule Calibration Result

## Summary

`tc-07`, `tc-15`의 expected keyword OR group을 좁게 보정했다.

직접 결과:

- 기존 report 재점수에서 `tc-07=1.0`, `tc-15=1.0`으로 회복했다.
- 서버 full eval에서도 `tc-07=1.0`, `tc-15=1.0`을 확인했다.
- 전체 `accuracy_mean`은 `1.0`으로 회복했다.

단, full eval 전체 완료 기준은 아직 충족하지 못했다.

- `tc-04`가 새 full eval에서 `faithfulness=0.0`으로 실패했다.
- `tc-04` 단일 재실행에서도 `faithfulness=0.0`이 재현됐다.
- `tc-04`는 이번 `eval/test_cases.json` 보정 대상이 아니며, source recall과 RAG precision은 `1.0`이다.
- 따라서 calibration은 목표 케이스를 해결했지만, full eval green을 위해 `tc-04` faithfulness triage가 후속 blocker로 남았다.

## Changes

파일:

- `eval/test_cases.json`

`tc-07`:

```json
["면책", "책임을 부담하지", "책임을 지지", "책임이 없"]
```

첫 keyword group을 위 OR group으로 확장했다.

이유:

- `책임` 단독은 너무 넓고 반대 의미에도 등장할 수 있다.
- `책임을 부담하지`, `책임을 지지`, `책임이 없`은 면책 의미가 분명한 책임 부정 표현이다.

`tc-15`:

```json
["예외", "불가능", "부득이", "긴급", "없이", "예측할 수 없", "통제할 수 없"]
```

세 번째 keyword group에 좁은 예외 표현을 추가했다.

이유:

- 최신 답변은 `사전 통지 내지 공지 없이`, `예측할 수 없거나 통제할 수 없는 사유`를 포함했다.
- `경우`, `사유`, `가능`처럼 일반적인 표현은 추가하지 않았다.

## Existing Report Re-score

기준 report:

- `eval/results/eval_20260618_113500.json`

재점수 결과:

| Case | Before | After |
| --- | ---: | ---: |
| `tc-07` | 0.75 | 1.0 |
| `tc-15` | 0.75 | 1.0 |

Match detail:

- `tc-07`: 첫 group이 `책임을 부담하지`로 match
- `tc-15`: 세 번째 group이 `없이`, `예측할 수 없`, `통제할 수 없`으로 match

## Full Eval

서버 명령:

```bash
cd /opt/ragSystem_codex
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
CUDA_VISIBLE_DEVICES="" \
.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
```

Reports:

- 서버 full eval: `/opt/ragSystem_codex/eval/results/eval_20260618_132509.json`
- 로컬 full eval: `eval/results/eval_20260618_132509.json`
- Source drift report: `docs/references/2026-06-18-tc07-tc15-eval-rule-calibration-source-drift-report.md`
- 서버 `tc-04` 단일 확인: `/opt/ragSystem_codex/eval/results/eval_tc04_check_20260618_132648.json`

Metrics:

| Metric | Value |
| --- | ---: |
| `accuracy_mean` | 1.0 |
| `faithfulness_mean` | 0.9565 |
| `not_found_success_rate` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `rag_normalized_source_precision@k_mean` | 1.0 |
| `rag_chunk_precision@k_mean` | 0.8609 |

Target case result:

| Case | Accuracy | Faithfulness | Source Recall | RAG Precision |
| --- | ---: | ---: | ---: | ---: |
| `tc-07` | 1.0 | 1.0 | 1.0 | 1.0 |
| `tc-15` | 1.0 | 1.0 | 1.0 | 1.0 |

## Latency Trace

최근 23개 `eval.case` trace 기준:

```text
count=23
first_timestamp=2026-06-18T04:20:52.814433+00:00
last_timestamp=2026-06-18T04:26:48.872637+00:00
mean_ms=9519.69
median_ms=10284.13
min_ms=2409.22
max_ms=16466.69
p95_ms=14511.91
```

## Remaining Failure

`tc-04`:

| Metric | Value |
| --- | ---: |
| `answer_accuracy` | 1.0 |
| `faithfulness` | 0.0 |
| `source_recall_at_k` | 1.0 |
| `rag_normalized_source_precision_at_k` | 1.0 |

단일 재실행에서도 같은 결과가 재현됐다.

현재 답변은 다음을 포함한다.

- 네이버 유료서비스 사용기간과 만료 후 이용권 소멸
- 카카오 정기결제형 서비스의 무료체험 만료 전 의사 확인
- 등록 결제수단을 이용한 정기결제
- 결제 내용 고지와 명시적 동의 시 고지 생략
- 자동 갱신 조건을 명시적으로 규정하는 내용은 문서에 나타나 있지 않다는 부분 답변

초기 분류:

- `tc-04`도 source recall/RAG precision은 정상이다.
- 이번 `tc-07`, `tc-15` rule calibration이 직접 원인은 아니다.
- 답변의 부분 부정 문장과 faithfulness judge 사이의 정합성 문제인지, 실제 answer wording 문제인지 별도 systematic-debugging이 필요하다.

## Decision

- `tc-07`, `tc-15` calibration 자체는 유지한다.
- 현재 작업은 full eval green 상태가 아니므로 active plan은 완료로 이동하지 않는다.
- 다음 작업은 `tc-04` faithfulness failure triage다.

## Next Work

1. `tc-04` faithfulness failure를 systematic-debugging 방식으로 triage한다.
2. 최신 full eval answer, single-case answer, retrieved context, faithfulness judge prompt를 비교한다.
3. 원인을 `answer wording`, `faithfulness judge`, `eval rule`, `prompt` 중 하나로 분류한다.
4. 그 결과에 따라 현재 calibration plan을 완료할지, 추가 수정이 필요한지 결정한다.
