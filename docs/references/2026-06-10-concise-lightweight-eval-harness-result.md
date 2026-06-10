# 2026-06-10 Concise Lightweight Eval Harness Result

## Summary

문서로 정의한 concise mode 경량 평가셋을 실행 가능한 eval harness로 반영했다.

구현 결과:

- `eval/concise_test_cases.json` 추가
- `eval/pipeline.py --concise-lightweight` 실행 경로 추가
- `answer_mode=concise`로만 RAG query 실행
- required point, forbidden claim, answer length, source count, no-answer 기준을 deterministic check로 판정
- 결과 JSON과 trace metadata에 `answer_mode=concise` 기록

## Implementation

### `eval/concise_test_cases.json`

6개 케이스를 추가했다.

- `concise-01`: 운영정책 계정 제한/해지 조건
- `concise-02`: 위치기반서비스 개인위치정보 이용 목적
- `concise-03`: 위치정보 동의 철회와 보유 기간
- `concise-04`: 유료서비스 청약철회/환불 제한
- `concise-05`: 유료서비스 자동 갱신 결제 주기/금액 no-answer
- `concise-06`: 유료서비스 중단/변경 통지

각 케이스는 아래 필드를 가진다.

- `required_points`
- `forbidden_claims`
- `expected_not_found`
- `max_answer_length`
- `min_source_count`

### `eval/pipeline.py`

추가한 실행 경로:

```bash
.venv/bin/python eval/pipeline.py --concise-lightweight --top-k 5 --model gemma3:12b
```

리포트 prefix:

```text
eval/results/concise_eval_*.json
```

trace route:

- `eval.concise`
- `eval.concise.case`

## Local Smoke Result

Command:

```bash
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/tmp/concise_eval_trace.jsonl \
.venv/bin/python eval/pipeline.py --concise-lightweight --top-k 5 --model gemma3:12b
```

Report:

```text
eval/results/concise_eval_20260610_092710.json
```

Summary:

| metric | value |
| --- | ---: |
| total_cases | 6 |
| passed_cases | 6 |
| pass_rate | 1.0 |
| required_points_score_mean | 0.875 |
| answer_length_mean | 315.0 |
| query_latency_ms_mean | 14343.675 |

Case summary:

| id | passed | required score | answer length | source count | query total ms | not_found_success |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `concise-01` | true | 1.0 | 313 | 5 | 17417.54 | null |
| `concise-02` | true | 0.75 | 240 | 5 | 11530.98 | null |
| `concise-03` | true | 0.75 | 338 | 5 | 15019.68 | null |
| `concise-04` | true | 1.0 | 370 | 5 | 14949.41 | null |
| `concise-05` | true | 1.0 | 325 | 5 | 13310.72 | true |
| `concise-06` | true | 0.75 | 304 | 5 | 13833.72 | null |

## Notes

- 로컬 Ollama는 작업 전 꺼져 있었고, smoke를 위해 `ollama serve`를 임시 기동했다가 종료했다.
- latency 권장 기준 12000ms는 pass/fail hard gate로 적용하지 않고 결과에 기록만 한다. cold load와 로컬 환경 차이가 크기 때문이다.
- standard full eval은 실행하지 않았다. 이번 변경은 concise 전용 eval 경로 추가이며 standard query 기본값은 변경하지 않았다.

## Validation

- 통과: `jq empty eval/concise_test_cases.json`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py query.py app.py`
- 통과: `bash scripts/validate-docs.sh`
- 통과: concise lightweight eval smoke

## Remaining Work

- Ubuntu 서버에 eval harness 변경분을 반영한다.
- 서버에서 `--concise-lightweight` smoke를 실행해 운영 GPU/Ollama 환경 기준 결과를 확인한다.
