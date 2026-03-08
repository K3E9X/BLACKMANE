#!/usr/bin/env bash
set -euo pipefail

# Resolve known PR #11 conflicts by keeping the branch (ours) versions
# for deployment/prod-ready files, then stage them.

FILES=(
  "README.md"
  "deploy/k8s/backend.yaml"
  "deploy/k8s/frontend.yaml"
  "deploy/k8s/ingress.yaml"
  "deploy/k8s/kustomization.yaml"
)

for f in "${FILES[@]}"; do
  if git ls-files --unmerged -- "$f" >/dev/null 2>&1 && [ -n "$(git ls-files --unmerged -- "$f")" ]; then
    echo "Resolving $f with --ours"
    git checkout --ours -- "$f"
  else
    echo "No conflict marker for $f (skipping checkout)"
  fi
done

git add "${FILES[@]}"

echo
echo "✅ Conflicts staged for selected files."
echo "Next steps:"
echo "  1) Review README.md manually if needed"
echo "  2) git commit -m 'Resolve PR #11 conflicts'"
echo "  3) git push"
