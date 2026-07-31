#!/bin/bash
# =============================================
# Launch AniShiv.com locally
# Usage: ./start_local.sh [port]
# Default port: 8000
# =============================================

PORT="${1:-8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

# Start local HTTP server
if command -v python3 &>/dev/null; then
  python3 -m http.server "$PORT"
elif command -v python &>/dev/null; then
  python -m http.server "$PORT"
elif command -v node &>/dev/null; then
  npx --yes http-server -p "$PORT" .
else
  echo "ERROR: Python 3, Python, or Node.js is required to run the local server."
  exit 1
fi
</｜｜DSML｜｜>