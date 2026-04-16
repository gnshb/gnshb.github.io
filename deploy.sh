#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMIT_MESSAGE="${1:-Update site on $(date '+%Y-%m-%d %H:%M:%S')}"

cd "$ROOT_DIR"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$1" >&2
    exit 1
  fi
}

require_cmd git
require_cmd python3

if [[ -n "$(git status --short --untracked-files=all)" ]]; then
  printf 'Building site...\n'
else
  printf 'No source changes detected. Nothing to deploy.\n'
  exit 0
fi

python3 build.py

for path in \
  "site/index.html" \
  "site/blog/index.html" \
  "site/projects/index.html"
do
  if [[ ! -f "$path" ]]; then
    printf 'Build check failed: missing %s\n' "$path" >&2
    exit 1
  fi
done

printf 'Local render looks complete.\n'

git add .

if git diff --cached --quiet; then
  printf 'No staged changes after build. Nothing to commit.\n'
  exit 0
fi

git commit -m "$COMMIT_MESSAGE"
git push origin main
printf 'Deploy complete.\n'
