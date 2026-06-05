# 2026-06-04 Gemma3 Top-K 3 Full Eval Result

## Summary

`gemma3:12b + top_k=3`은 query latency를 낮추지만 품질 기준선을 만족하지 못했다.

최종 판단:

- `top_k=3`은 운영 전환 후보로 채택하지 않는다.
- `tc-07`, `tc-11` smoke 회복은 full eval 전체 품질로 일반화되지 않았다.
- 속도 개선의 1차 후보는 여전히 `gemma3:12b` 계열이지만, `top_k=3` 고정은 source recall 회귀가 크다.

## Environment

- 실행 위치: Ubuntu 서버 `/opt/ragSystem_codex`
- 실행일: 2026-06-04
- 모델: `gemma3:12b`
- `top_k`: 3
- 리포트: `eval/results/eval_20260604_171559.json`
- 로컬 복사본: `eval/results/eval_20260604_171559.json`
- trace path: `/opt/ragSystem_codex/logs/rag_traces.jsonl`

Pre-flight note:

- 서버 `gemma3:12b`는 설치되어 있었다.
- 기준선 `eval/results/eval_20260602_131307.json`은 존재했다.
- 서버 API `/health`는 `model=gemma4:e4b`였다. 기존 계획의 기대값 `gemma4:26b`와 달랐지만, 이번 eval은 CLI `--model gemma3:12b --top-k 3` 경로라 운영 API 모델은 변경하지 않았다.

## Command

```bash
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
CUDA_VISIBLE_DEVICES="" \
.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 3
```

평가 Python 프로세스만 CPU 모드로 실행해 임베딩/reranker가 GPU를 추가 점유하지 않도록 했다. Ollama 서비스의 GPU 사용 가능 여부는 변경하지 않았다.

## Metrics

| Metric | `gemma3:12b top_k=5` baseline | `gemma3:12b top_k=3` | Result |
| --- | ---: | ---: | --- |
| `accuracy_mean` | 0.9891 | 0.942 | Regressed |
| `faithfulness_mean` | 0.9565 | 0.9565 | Same |
| `not_found_success_rate` | 1.0 | 1.0 | Same |
| `source_recall@k_mean` | 1.0 | 0.8449 | Regressed |
| `source_coverage@k_mean` | 1.0 | 0.8449 | Regressed |
| `rag_normalized_source_precision@k_mean` | 1.0 | 0.9058 | Regressed |
| `rag_chunk_precision@k_mean` | 0.8609 | 0.8696 | Slightly improved |

The improved `precision@k` and `rag_precision@k` values are partly a denominator effect from reducing `k` to 3. The stronger signal is the `source_recall@k_mean` regression.

## Trace Latency

Trace `eval.case` rows for this run:

- count: 23
- mean `query_total`: about 8.7s
- median `query_total`: about 8.5s
- min `query_total`: about 1.8s
- max `query_total`: about 20.1s
- p95 `query_total`: about 15.2s

This confirms a latency benefit versus the earlier `gemma3:12b top_k=5` API smoke at about 29.0s total. The quality regression is the blocker.

## Regressed Cases

Answer metric regressions:

- `tc-04`: `answer_accuracy=0.0`, `faithfulness=0.0`
- `tc-17`: `answer_accuracy=0.6667`, `faithfulness=1.0`

Source recall regressions include:

- `tc-02`: `source_recall_at_k=0.6`
- `tc-03`: `source_recall_at_k=0.75`
- `tc-05`: `source_recall_at_k=0.5`
- `tc-06`: `source_recall_at_k=0.75`
- `tc-09`: `source_recall_at_k=0.5`
- `tc-10`: `source_recall_at_k=0.5`
- `tc-14`: `source_recall_at_k=0.75`
- `tc-15`: `source_recall_at_k=0.75`
- `tc-17`: `source_recall_at_k=0.6667`
- `tc-19`: `source_recall_at_k=0.6667`

## Decision

Do not change the operating `top_k` to 3.

`top_k=3` is fast, but it removes enough relevant source coverage to degrade the broader evaluation set. The two-case smoke was useful but insufficient as a promotion gate.

## Next Work

Recommended next options:

1. Compare `gemma3:12b + top_k=5` as the primary operating model candidate against the current operating model, accepting that quality is not perfect but latency is much better.
2. Run a focused `top_k=4` experiment if the goal is to find a middle point between source recall and latency.
3. Separately test API CPU mode for embedding/reranker to reduce GPU memory competition with Ollama, especially if keeping a `gemma4` operating model.
