#!/usr/bin/env bash
# Check that the site builds, then commit everything and push.
# GitHub builds and deploys the site when main is pushed.
#
# Usage: ./publish.sh "What changed"

set -euo pipefail
cd "$(dirname "$0")"

message="${1:-Update site}"

if command -v hugo >/dev/null 2>&1; then
  echo "Checking the build..."
  out="$(mktemp -d)"
  trap 'rm -rf "$out"' EXIT
  if ! log="$(hugo --logLevel warn --destination "$out" 2>&1)"; then
    echo "$log"
    echo "The build failed, so nothing was committed. Fix the error above and try again."
    exit 1
  fi
  grep -E "WARN" <<< "$log" || true
else
  echo "Hugo isn't installed, so skipping the local check (GitHub will still build the site)."
fi

git add -A
if git diff --cached --quiet; then
  echo "Nothing to publish."
  exit 0
fi

git commit -m "$message"
git push origin HEAD
echo "Pushed. The site updates in a minute or two once GitHub has built it."
