#!/usr/bin/env bash
set -euo pipefail

UNMERGED=$(git diff --name-only --diff-filter=U || true)

if [ -z "$UNMERGED" ]; then
  echo "✅ Aucun conflit Git en cours (index clean côté merge)."
  exit 0
fi

echo "⚠️ Fichiers en conflit :"
echo "$UNMERGED" | sed 's/^/ - /'

echo
echo "Marqueurs détectés (si présents dans le working tree) :"
while IFS= read -r f; do
  [ -z "$f" ] && continue
  rg -n "^(<<<<<<<|=======|>>>>>>>)" "$f" || true
done <<< "$UNMERGED"

exit 1
