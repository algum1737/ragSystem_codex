# 2026-06-10 Concise Eval Server Verification Result

## Summary

로컬에서 구현한 concise lightweight eval harness를 Ubuntu 서버에 반영하고 운영 GPU/Ollama 환경에서 smoke를 실행했다.

결론:

- 서버 파일 반영, JSON 검증, Python compile이 통과했다.
- 서버 `--concise-lightweight` smoke는 6개 케이스 모두 통과했다.
- trace route `eval.concise`와 `eval.concise.case`가 별도 trace 파일에 기록됐다.
- 운영 API `/health`는 smoke 이후에도 정상이다.

## Environment

- Server: `10.10.220.5`
- User: `ragadmin`
- App path: `/opt/ragSystem_codex`
- Model: `gemma3:12b`
- top_k: `5`
- Trace path: `/opt/ragSystem_codex/logs/concise_lightweight_eval_20260610.jsonl`
- Report: `/opt/ragSystem_codex/eval/results/concise_eval_20260610_105027.json`

## Files Applied

- `eval/pipeline.py`
- `eval/concise_test_cases.json`

## Validation

서버에서 Python 기반 JSON 확인과 compile을 실행했다. 서버에는 `jq`가 없어 Python JSON load로 대체했다.

```bash
cd /opt/ragSystem_codex
.venv/bin/python - <<'PY'
import json
from pathlib import Path
cases=json.loads(Path('eval/concise_test_cases.json').read_text(encoding='utf-8'))['cases']
print('json_ok')
print('concise_cases', len(cases))
print('pipeline_size', Path('eval/pipeline.py').stat().st_size)
PY
.venv/bin/python -m py_compile eval/pipeline.py
```

Result:

```text
json_ok
concise_cases 6
pipeline_size 29538
```

## Smoke Command

```bash
cd /opt/ragSystem_codex
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/opt/ragSystem_codex/logs/concise_lightweight_eval_20260610.jsonl \
.venv/bin/python eval/pipeline.py --concise-lightweight --top-k 5 --model gemma3:12b
```

## Smoke Summary

| metric | value |
| --- | ---: |
| total_cases | 6 |
| passed_cases | 6 |
| pass_rate | 1.0 |
| required_points_score_mean | 0.875 |
| answer_length_mean | 315.3333 |
| query_latency_ms_mean | 8483.0783 |

## Case Summary

| id | passed | required score | answer length | source count | query total ms | not_found_success |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `concise-01` | true | 1.0 | 309 | 5 | 22252.60 | null |
| `concise-02` | true | 0.75 | 268 | 5 | 5117.19 | null |
| `concise-03` | true | 0.75 | 376 | 5 | 6542.73 | null |
| `concise-04` | true | 1.0 | 342 | 5 | 6724.65 | null |
| `concise-05` | true | 1.0 | 339 | 5 | 5703.46 | true |
| `concise-06` | true | 0.75 | 258 | 5 | 4557.84 | null |

## Trace Check

Trace tail에서 아래를 확인했다.

- route `eval.concise`
- route `eval.concise.case`
- metadata `answer_mode=concise`
- `eval_case_id` for case-level trace
- `eval_scores.passed=true`

## Runtime Health

Smoke 이후 API health:

```text
{"status":"ok","model":"gemma3:12b"}
```

## Notes

- `concise-01`은 첫 케이스라 model/cold-load 영향으로 22252.60ms가 걸렸다.
- 이후 warmed 케이스는 약 4.6초에서 6.7초 사이였다.
- full eval은 실행하지 않았다. 이번 작업은 concise 전용 eval harness의 서버 smoke 검증이다.

## Decision

서버 반영과 smoke는 완료됐다. 다음 판단은 이 lightweight eval을 CI나 배포 후 수동 검증 루프에 승격할지 여부다.
