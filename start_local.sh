#!/bin/bash
# =============================================
# Launch AniShiv.com locally
# Usage: ./start_local.sh [port]
# Default port: 8000
# =============================================

PORT="${1:-8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

find_available_port() {
  local start_port="$1"
  local probe_port
  for ((probe_port=start_port; probe_port<start_port+50; probe_port++)); do
    if ! lsof -iTCP:"$probe_port" -sTCP:LISTEN -t >/dev/null 2>&1; then
      echo "$probe_port"
      return 0
    fi
  done

  return 1
}

if lsof -iTCP:"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  NEXT_PORT="$(find_available_port "$PORT")"
  if [[ -z "$NEXT_PORT" ]]; then
    echo "ERROR: No available port found in range $PORT-$((PORT+49))."
    exit 1
  fi
  echo "Port $PORT is already in use. Switching to available port $NEXT_PORT."
  PORT="$NEXT_PORT"
fi

cd "$SCRIPT_DIR"

echo "=============================================="
echo "  AniShiv.com - Local Server"
echo "  URL: http://localhost:$PORT"
echo "  Press Ctrl+C to stop."
echo "=============================================="

# Open the browser automatically (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
  open "http://localhost:$PORT" 2>/dev/null &
fi

# Start local server.
# Prefer PHP so form handlers (e.g., contact_submit.php) work locally.
if command -v php &>/dev/null; then
  php -S "localhost:$PORT" -t . local_router.php
elif command -v python3 &>/dev/null; then
  echo "WARNING: Using static server; PHP endpoints will not execute."
  python3 -m http.server "$PORT"
elif command -v python &>/dev/null; then
  echo "WARNING: Using static server; PHP endpoints will not execute."
  python -m http.server "$PORT"
elif command -v node &>/dev/null; then
  echo "WARNING: Using static server; PHP endpoints will not execute."
  npx --yes http-server -p "$PORT" .
else
  echo "ERROR: PHP, Python 3, Python, or Node.js is required to run the local server."
  exit 1
fi