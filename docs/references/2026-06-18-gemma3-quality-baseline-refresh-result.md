# 2026-06-18 Gemma3 Quality Baseline Refresh Result

## Summary

`gemma3:12b + top_k=5` 최신 full eval을 재실행했다.

결론:

- retrieval/source 지표는 정상이다.
- faithfulness와 not-found는 기준을 만족한다.
- `accuracy_mean`은 `0.9783`으로 이전 `gemma3:12b + top_k=5` 기준선 `0.9891`보다 낮다.
- 회귀/약점은 `tc-07`, `tc-15` 두 케이스이며 둘 다 `source_recall_at_k=1.0`, `rag_normalized_source_precision_at_k=1.0`, `faithfulness=1.0`이다.
- 따라서 다음 개선 후보는 retrieval 변경이나 모델 교체가 아니라 `tc-07`, `tc-15`의 answer wording과 eval rule 정합성 triage다.

## Environment

- 실행 위치: Ubuntu 서버 `/opt/ragSystem_codex`
- 실행일: 2026-06-18
- 모델: `gemma3:12b`
- `top_k`: 5
- Chroma count: 318
- API health: `{"status":"ok","model":"gemma3:12b"}`
- Streamlit health: `ok`

## Commands

Full eval:

```bash
cd /opt/ragSystem_codex
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
CUDA_VISIBLE_DEVICES="" \
.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
```

Source drift report:

```bash
.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260618_113500.json \
  --test-cases eval/test_cases.json \
  --output docs/references/2026-06-18-gemma3-quality-baseline-source-drift-report.md
```

## Reports

- 서버 eval report: `/opt/ragSystem_codex/eval/results/eval_20260618_113500.json`
- 로컬 eval report: `eval/results/eval_20260618_113500.json`
- Source drift report: `docs/references/2026-06-18-gemma3-quality-baseline-source-drift-report.md`

## Metrics

| Metric | Previous `gemma3:12b top_k=5` | Latest `gemma3:12b top_k=5` | Result |
| --- | ---: | ---: | --- |
| `accuracy_mean` | 0.9891 | 0.9783 | Regressed |
| `faithfulness_mean` | 0.9565 | 1.0000 | Improved |
| `not_found_success_rate` | 1.0000 | 1.0000 | Same |
| `source_recall@k_mean` | 1.0000 | 1.0000 | Same |
| `source_coverage@k_mean` | 1.0000 | 1.0000 | Same |
| `rag_normalized_source_precision@k_mean` | 1.0000 | 1.0000 | Same |
| `rag_chunk_precision@k_mean` | 0.8609 | 0.8609 | Same |

## Latency Trace

최근 23개 `eval.case` trace 기준:

```text
count=23
first_timestamp=2026-06-18T02:30:12.303614+00:00
last_timestamp=2026-06-18T02:35:00.989808+00:00
mean_ms=11219.67
median_ms=11143.97
min_ms=2666.06
max_ms=28507.23
p95_ms=17250.61
```

## Critical Cases

Source drift report 기준 critical case:

| Case | Accuracy | Faithfulness | Source Recall | RAG Precision | Primary Classification |
| --- | ---: | ---: | ---: | ---: | --- |
| `tc-07` | 0.7500 | 1.0000 | 1.0000 | 1.0000 | `eval rule` / `answer wording` |
| `tc-15` | 0.7500 | 1.0000 | 1.0000 | 1.0000 | `eval rule` / `answer wording` |

Watch case는 없다.

## Case Notes

### `tc-07`

질문은 위치기반서비스 약관의 면책 조항을 묻는다.

최신 답변은 다음 근거를 충실히 포함했다.

- 천재지변 또는 불가항력
- 제3자의 고의적인 서비스 방해
- 이용자 귀책사유
- 회사의 고의·과실 없는 사유
- 신뢰도/정확성 보증 부재
- 이용자 손해에 대한 책임 부재

하지만 `expected_keywords`의 고정 표지어 `면책`을 직접 포함하지 않아 `0.75`가 됐다. 이전 기준선에서도 같은 패턴이었으므로 새 retrieval/source 회귀는 아니다.

### `tc-15`

질문은 일반 서비스 약관에서 서비스 변경/종료 시 사전 고지 없이 가능한 예외를 묻는다.

최신 답변은 다음 내용을 포함했다.

- 정기/임시 점검, 정전, 설비 장애, 이용량 폭주
- 관계사 계약 종료, 정부 명령/규제, 정책 변경
- 천재지변, 국가비상사태 등 불가항력
- 예측할 수 없거나 통제할 수 없는 사유
- 사전 통지 내지 공지 없이 중단 가능

하지만 `expected_keywords`의 세 번째 그룹인 `예외`, `불가능`, `부득이`, `긴급` 중 하나를 직접 포함하지 않아 `0.75`가 됐다. 이전 기준선에서는 같은 케이스가 `1.0`이었다.

## Decision

- 운영 모델 변경은 하지 않는다.
- retrieval, reranker, chunking 변경도 하지 않는다.
- 현재 실패는 source 누락이 아니라 faithful answer의 wording과 deterministic accuracy rule 사이의 정합성 문제로 분류한다.
- 다음 작업은 `tc-07`, `tc-15`를 대상으로 answer wording 보강이 맞는지, eval rule 보정이 맞는지 systematic-debugging 방식으로 좁히는 것이다.

## Next Work

다음 후보:

1. `tc-07`, `tc-15` focused triage active plan을 작성한다.
2. 두 케이스의 현 답변, expected keyword, retrieved context를 비교한다.
3. 후보를 둘 중 하나로 제한한다.
   - eval rule 보정: 실제 답변이 충분히 유효한 경우 deterministic keyword group을 좁게 확장
   - answer wording 보강: 사용자 질문의 핵심 법률 표지어를 근거가 있을 때 답변에 보존하도록 prompt를 최소 수정
4. 어떤 후보든 full eval 또는 focused smoke 이후에만 적용한다.
