#!/usr/bin/env bash
set -euo pipefail

# Resolve known recurring conflicts for PR #11 style merges.
# Default strategy: keep branch version (--ours) on docs/deploy conflict files.

UNMERGED=$(git diff --name-only --diff-filter=U || true)
if [ -z "$UNMERGED" ]; then
  echo "✅ Aucun conflit détecté."
  exit 0
fi

echo "Conflits détectés:"
echo "$UNMERGED" | sed 's/^/ - /'

resolved=0
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in
    README.md|deploy/k8s/backend.yaml|deploy/k8s/frontend.yaml|deploy/k8s/ingress.yaml|deploy/k8s/kustomization.yaml)
      echo "Resolving $f with --ours"
      git checkout --ours -- "$f"
      git add "$f"
      resolved=$((resolved+1))
      ;;
    *)
      echo "Skipping unknown conflict file: $f"
      ;;
  esac
done <<< "$UNMERGED"

remaining=$(git diff --name-only --diff-filter=U || true)
if [ -n "$remaining" ]; then
  echo
  echo "❌ Conflits restants à résoudre manuellement:"
  echo "$remaining" | sed 's/^/ - /'
  exit 2
fi

echo
printf "✅ %d fichier(s) conflit résolu(s) et stage(s).\n" "$resolved"
echo "Next: git commit -m 'Resolve merge conflicts' && git push"
