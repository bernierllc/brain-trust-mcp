#!/usr/bin/env bash
set -euo pipefail

echo "🔍 brain-trust smoke test"
URL="${1:-http://localhost:8000/health}"

echo "→ Checking health at: $URL"
HTTP_CODE=$(curl -s -o /tmp/health.json -w "%{http_code}" "$URL" || true)

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "❌ Health endpoint returned HTTP $HTTP_CODE"
  exit 1
fi

echo "✅ Health OK"
cat /tmp/health.json | sed 's/{/\n{/; s/,/\n  ,/g'

exit 0
