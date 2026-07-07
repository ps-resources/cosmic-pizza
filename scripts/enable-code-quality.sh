#!/usr/bin/env bash
#
# Enable GitHub Code Quality across many repositories at once.
#
# Code Quality exposes a REST API to enable it per repository:
#   PATCH /repos/{owner}/{repo}/code-quality/setup
# This script loops over a CSV of repositories and, for each one, asks GitHub
# which languages the repo uses, keeps the ones Code Quality supports, and calls
# that endpoint with exactly those languages. Handy when you want to roll Code
# Quality out to a specific *subset* of repos (rather than the whole org via the
# org-level toggle).
#
# NOTE: The Code Quality REST API is in PUBLIC PREVIEW and uses the dated API
# version 2026-03-10. Both may change before general availability (2026-07-20).
#
# Prerequisites:
#   * gh CLI authenticated as a user/admin who can configure the target repos
#     (gh auth login). The token needs the `repo` scope.
#   * Code Quality must be allowed for the org/enterprise that owns the repos.
#   * GitHub Actions must be enabled on each repo (Code Quality runs on Actions).
#     NOTE: this script enables Code Quality but does NOT enable Actions. If a
#     repo has Actions turned off, the PATCH below still succeeds but no scan
#     ever runs, so the repo stays blank on the dashboard. Turn Actions on first.
#
# Heads up — enablement is ASYNCHRONOUS. A successful request only *requests*
# setup; the first CodeQL scan runs afterward on Actions and the org dashboard
# fills in only once those scans complete. Run this well ahead of any demo.
#
# Usage:
#   ./scripts/enable-code-quality.sh [path/to/repos.csv]
#
# CSV format (one repository per line, "owner/repo"), with a header row:
#   repository
#   my-org/service-a
#   my-org/service-b

set -euo pipefail

CSV_FILE="${1:-scripts/repos.csv}"
API_VERSION="2026-03-10"

# Map a language name as reported by the GitHub "languages" API to the matching
# CodeQL identifier that Code Quality understands. Languages that Code Quality
# does NOT support return nothing and are skipped.
#
# Code Quality-supported CodeQL languages:
#   csharp, go, java-kotlin, javascript-typescript, python, ruby
map_language() {
  case "$1" in
    "C#")                     echo "csharp" ;;
    "Go")                     echo "go" ;;
    "Java" | "Kotlin")        echo "java-kotlin" ;;
    "JavaScript" | "TypeScript") echo "javascript-typescript" ;;
    "Python")                 echo "python" ;;
    "Ruby")                   echo "ruby" ;;
    *)                        : ;; # unsupported -> ignored
  esac
}

if [[ ! -f "$CSV_FILE" ]]; then
  echo "❌ CSV file not found: $CSV_FILE" >&2
  exit 1
fi

echo "Enabling Code Quality for repositories listed in: $CSV_FILE"
echo

# Skip the header row, ignore blank lines and #-comment lines.
tail -n +2 "$CSV_FILE" | tr -d '\r' | while IFS= read -r repo; do
  [[ -z "$repo" ]] && continue
  [[ "$repo" == \#* ]] && continue

  echo "→ $repo"

  # 1) Ask GitHub which languages the repo actually uses, then keep only the
  #    ones Code Quality supports (mapped to their CodeQL identifiers, deduped).
  detected="$(
    gh api \
      -H "Accept: application/vnd.github+json" \
      "/repos/${repo}/languages" --jq 'keys[]' 2>/dev/null \
    | while IFS= read -r lang; do map_language "$lang"; done \
    | sed '/^$/d' | sort -u
  )"

  if [[ -z "$detected" ]]; then
    echo "   ⚠️  Skipped (no Code Quality-supported languages detected, or the"
    echo "       repo could not be read — check the name and your access)"
    continue
  fi

  # 2) Turn the detected languages into repeated -f languages[]=... arguments.
  lang_args=()
  while IFS= read -r cq_lang; do
    lang_args+=(-f "languages[]=${cq_lang}")
  done <<< "$detected"

  echo "   Languages: $(echo "$detected" | tr '\n' ' ')"

  # 3) Enable Code Quality for exactly those languages.
  #    Capture stderr so that if the request fails we can show the real API
  #    error (e.g. an org/enterprise policy wall) instead of a generic message.
  if api_error="$(
      gh api \
        --method PATCH \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: ${API_VERSION}" \
        "/repos/${repo}/code-quality/setup" \
        -f "state=configured" \
        "${lang_args[@]}" \
        2>&1 >/dev/null)"; then
    echo "   ✅ Code Quality enablement requested"
  else
    echo "   ⚠️  Failed (check that the repo exists, Actions is enabled, and"
    echo "       Code Quality is allowed for the owning org/enterprise)"
    if [[ -n "$api_error" ]]; then
      echo "       API error: ${api_error}"
    fi
  fi
done

echo
echo "Done. Re-run with a different CSV to target another set of repositories."
echo "Tip: confirm a single repo's status with:"
echo "  gh api -H \"X-GitHub-Api-Version: ${API_VERSION}\" /repos/OWNER/REPO/code-quality/setup"
