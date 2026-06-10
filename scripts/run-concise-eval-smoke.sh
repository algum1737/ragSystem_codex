#!/usr/bin/env bash

set -euo pipefail

APP_DIR="${APP_DIR:-/opt/ragSystem_codex}"
MODEL="${MODEL:-gemma3:12b}"
TOP_K="${TOP_K:-5}"
STAMP="${STAMP:-$(date +%Y%m%d_%H%M%S)}"
TRACE_PATH="${TRACE_PATH:-${APP_DIR}/logs/concise_lightweight_eval_${STAMP}.jsonl}"
PYTHON_BIN="${PYTHON_BIN:-${APP_DIR}/.venv/bin/python}"

cd "${APP_DIR}"

mkdir -p "${APP_DIR}/logs" "${APP_DIR}/eval/results"

echo "[concise-eval] app_dir=${APP_DIR}"
echo "[concise-eval] model=${MODEL}"
echo "[concise-eval] top_k=${TOP_K}"
echo "[concise-eval] trace_path=${TRACE_PATH}"

"${PYTHON_BIN}" - <<'PY'
import json
from pathlib import Path

cases = json.loads(Path("eval/concise_test_cases.json").read_text(encoding="utf-8"))["cases"]
print(f"[concise-eval] concise_cases={len(cases)}")
PY

"${PYTHON_BIN}" -m py_compile eval/pipeline.py

before="$(find eval/results -maxdepth 1 -name 'concise_eval_*.json' -type f -print | sort | tail -n 1 || true)"

RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH="${TRACE_PATH}" \
"${PYTHON_BIN}" eval/pipeline.py --concise-lightweight --top-k "${TOP_K}" --model "${MODEL}"

after="$(find eval/results -maxdepth 1 -name 'concise_eval_*.json' -type f -print | sort | tail -n 1 || true)"

if [[ -z "${after}" ]]; then
  echo "[concise-eval] no concise eval report found" >&2
  exit 1
fi

if [[ "${after}" == "${before}" ]]; then
  echo "[concise-eval] latest report did not change: ${after}" >&2
  exit 1
fi

echo "[concise-eval] report=${after}"

"${PYTHON_BIN}" - "${after}" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1])
data = json.loads(report.read_text(encoding="utf-8"))
summary = data["summary"]
print("[concise-eval] summary")
for key in (
    "total_cases",
    "passed_cases",
    "pass_rate",
    "required_points_score_mean",
    "answer_length_mean",
    "query_latency_ms_mean",
):
    print(f"[concise-eval]   {key}={summary.get(key)}")

if summary.get("total_cases") != summary.get("passed_cases"):
    raise SystemExit("[concise-eval] failed: not all concise cases passed")
PY

if [[ ! -s "${TRACE_PATH}" ]]; then
  echo "[concise-eval] trace file was not created or is empty: ${TRACE_PATH}" >&2
  exit 1
fi

echo "[concise-eval] trace_tail"
tail -n 2 "${TRACE_PATH}"
