#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-ragsystem-api.service}"
APP_DIR="${APP_DIR:-/opt/ragSystem_codex}"
TRACE_PATH="${RAG_TRACE_PATH:-${APP_DIR}/logs/rag_traces.jsonl}"
API_HEALTH_URL="${API_HEALTH_URL:-http://localhost:8000/health}"
OVERRIDE_DIR="/etc/systemd/system/${SERVICE_NAME}.d"
OVERRIDE_FILE="${OVERRIDE_DIR}/trace.conf"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "error: root 권한이 필요합니다. 예: sudo bash $0" >&2
  exit 1
fi

if [[ ! -d "${APP_DIR}" ]]; then
  echo "error: APP_DIR이 없습니다: ${APP_DIR}" >&2
  exit 1
fi

mkdir -p "${APP_DIR}/logs"
mkdir -p "${OVERRIDE_DIR}"

cat > "${OVERRIDE_FILE}" <<EOF
[Service]
Environment=RAG_TRACE_ENABLED=true
Environment=RAG_TRACE_PATH=${TRACE_PATH}
EOF

systemctl daemon-reload
systemctl restart "${SERVICE_NAME}"
systemctl --no-pager --full status "${SERVICE_NAME}" || true
curl -fsS "${API_HEALTH_URL}"
echo

echo "trace override: ${OVERRIDE_FILE}"
echo "trace path: ${TRACE_PATH}"
if [[ -f "${TRACE_PATH}" ]]; then
  tail -n 5 "${TRACE_PATH}"
else
  echo "trace file is not created yet. Run one query, then check:"
  echo "tail -n 5 ${TRACE_PATH}"
fi
