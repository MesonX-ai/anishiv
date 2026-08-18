#!/bin/bash
# =============================================
# submit_indexnow - Submit AniShiv.com URLs to Bing / Yandex / Seznam
# via the IndexNow protocol for fast indexing.
#
# Run this AFTER publishing the site (./publish_site) so Bing crawls the
# new/updated pages immediately.
# =============================================
set -euo pipefail

cd "$(dirname "$0")"

# The IndexNow key file must be published at https://www.anishiv.com/<KEY>.txt
KEY_FILE="$(ls [0-9a-f]*.txt 2>/dev/null | grep -v -E '^(ads|robots)\.txt$' | head -1 || true)"
if [[ -z "$KEY_FILE" ]]; then
  echo "ERROR: IndexNow key file (*.txt) not found in this directory." >&2
  exit 1
fi
KEY="${KEY_FILE%.txt}"
HOST="www.anishiv.com"
BASE="https://$HOST"

URLS=(
  "$BASE/"
  "$BASE/shiva-dhanuskodi.htm"
  "$BASE/mesonsoft-llc.htm"
  "$BASE/projects.htm"
  "$BASE/aboutus.htm"
  "$BASE/contactus.htm"
  "$BASE/photogallery.htm"
  "$BASE/privacy_policy.htm"
)

# Build the JSON payload
JSON="{\"host\":\"$HOST\",\"key\":\"$KEY\",\"keyLocation\":\"$BASE/$KEY.txt\",\"urlList\":["
for u in "${URLS[@]}"; do JSON+="\"$u\","; done
JSON="${JSON%,}]}"

echo "Submitting ${#URLS[@]} URLs to IndexNow (key file: $KEY.txt)..."
curl -sS -o /dev/null -w "IndexNow HTTP status: %{http_code}\n" \
  -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$JSON"
echo "Done. HTTP 200 = submitted successfully; 202 = accepted."