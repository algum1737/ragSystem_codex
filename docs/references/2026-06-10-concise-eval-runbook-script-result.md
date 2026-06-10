# 2026-06-10 Concise Eval Runbook Script Result

## Summary

서버 concise lightweight eval smoke를 반복 실행하기 위한 script와 runbook을 추가했다.

추가 결과:

- `scripts/run-concise-eval-smoke.sh` 추가
- `docs/manual-deployment-guide.md`에 `Concise Eval Smoke` 절차 추가
- 서버 `/opt/ragSystem_codex/scripts/run-concise-eval-smoke.sh`에 script 반영
- 서버에서 script를 실제 실행해 report/trace 생성과 failure detection을 확인

## Script

Script:

```bash
bash scripts/run-concise-eval-smoke.sh
```

주요 환경변수:

- `APP_DIR`: 기본 `/opt/ragSystem_codex`
- `MODEL`: 기본 `gemma3:12b`
- `TOP_K`: 기본 `5`
- `STAMP`: 기본 현재 시각
- `TRACE_PATH`: 기본 `${APP_DIR}/logs/concise_lightweight_eval_${STAMP}.jsonl`
- `PYTHON_BIN`: 기본 `${APP_DIR}/.venv/bin/python`

Script 동작:

1. concise eval case JSON을 읽어 case 수를 출력한다.
2. `eval/pipeline.py`를 compile한다.
3. `RAG_TRACE_ENABLED=true`와 별도 trace path로 `--concise-lightweight`를 실행한다.
4. 새 `eval/results/concise_eval_*.json` report가 생성됐는지 확인한다.
5. summary를 출력한다.
6. 모든 concise case가 통과하지 않으면 실패한다.
7. trace file이 생성됐는지 확인하고 tail을 출력한다.

## Server Verification

서버에 script와 최신 concise case JSON을 반영했다.

```bash
scp scripts/run-concise-eval-smoke.sh ragadmin@10.10.220.5:/opt/ragSystem_codex/scripts/run-concise-eval-smoke.sh
scp eval/concise_test_cases.json ragadmin@10.10.220.5:/opt/ragSystem_codex/eval/concise_test_cases.json
```

실행 명령:

```bash
cd /opt/ragSystem_codex
STAMP=20260610_runbook_test2 bash scripts/run-concise-eval-smoke.sh
```

Result:

```text
total_cases=6
passed_cases=5
pass_rate=0.8333
required_points_score_mean=0.7917
answer_length_mean=326.8333
query_latency_ms_mean=7201.0217
```

Report:

```text
/opt/ragSystem_codex/eval/results/concise_eval_20260610_114205.json
```

Trace:

```text
/opt/ragSystem_codex/logs/concise_lightweight_eval_20260610_runbook_test2.jsonl
```

## Failure Detected

Script는 `concise-06` 실패를 잡고 exit code 1로 종료했다.

실패 원인:

- 질문: `유료서비스 약관에서 서비스 제공 중단 또는 서비스 변경 시 회원에게 어떻게 통지하는가?`
- 답변은 유료서비스 변경/중단과 통지를 언급했다.
- 하지만 통지 수단 required point는 `정한 방법` 1개만 충족했고, `전자우편`, `카카오톡`, `게시판`, `팝업`, `제6조` 등 구체 수단을 충분히 언급하지 않았다.
- 사전 통지 원칙과 부득이한 경우 사후 통지 예외도 누락했다.

이 실패는 script 오류가 아니라 concise 답변 품질 또는 prompt/required point 조정이 필요한 실제 triage 대상이다.

## Runtime Health

실패 후 운영 API health는 정상이다.

```text
{"status":"ok","model":"gemma3:12b"}
```

## Validation

- 통과: `bash -n scripts/run-concise-eval-smoke.sh`
- 통과: `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`
- 통과: `bash scripts/validate-docs.sh`
- 통과: 서버 script 반영
- 통과: 서버 script가 report와 trace를 생성하고 failing case를 비정상 종료로 감지

## Decision

Runbook/script 작업은 완료됐다. 다음 작업은 `concise-06` 실패를 triage해 prompt 문제인지 평가 기준 문제인지 결정하는 것이다.
