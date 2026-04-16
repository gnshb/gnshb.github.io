#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_URL="https://gnshb.github.io"
WORKFLOW_NAME="Deploy Site"
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
require_cmd gh
require_cmd curl

if ! gh auth status >/dev/null 2>&1; then
  printf 'GitHub CLI is not authenticated. Run: gh auth login\n' >&2
  exit 1
fi

if [[ -n "$(git status --short --untracked-files=all)" ]]; then
  printf 'Preparing local build...\n'
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

HEAD_SHA="$(git rev-parse HEAD)"
RUN_ID=""

printf 'Waiting for GitHub Actions run for %s...\n' "$HEAD_SHA"
for _ in $(seq 1 30); do
  RUN_ID="$(gh run list \
    --workflow "$WORKFLOW_NAME" \
    --limit 20 \
    --json databaseId,headSha \
    --jq ".[] | select(.headSha == \"$HEAD_SHA\") | .databaseId" | head -n 1)"
  if [[ -n "$RUN_ID" ]]; then
    break
  fi
  sleep 2
done

if [[ -z "$RUN_ID" ]]; then
  printf 'Could not find the workflow run for commit %s\n' "$HEAD_SHA" >&2
  exit 1
fi

gh run watch "$RUN_ID" --exit-status

check_url() {
  local url="$1"
  local expected="$2"
  local html=""

  for _ in $(seq 1 30); do
    if html="$(curl -fsSL "$url")"; then
      if grep -Fq "$expected" <<<"$html"; then
        printf 'OK %s\n' "$url"
        return 0
      fi
    fi
    sleep 2
  done

  printf 'Verification failed for %s\n' "$url" >&2
  return 1
}

printf 'Checking live pages...\n'
check_url "$SITE_URL/" "Ganesh Balaji"
check_url "$SITE_URL/blog/" "Posts in reverse chronological order."
check_url "$SITE_URL/projects/" "Selected work."

printf 'Deploy complete.\n'
