#!/usr/bin/env bash
#
# Enable GitHub Code Quality across many repositories at once.
#
# Code Quality exposes a REST API to enable it per repository:
#   PATCH /repos/{owner}/{repo}/code-quality/setup
# This script loops over a CSV of repositories and calls that endpoint for each,
# which is handy when you want to roll Code Quality out to a specific *subset* of
# repos (rather than the whole org via the org-level toggle).
#
# NOTE: The Code Quality REST API is in PUBLIC PREVIEW and uses the dated API
# version 2026-03-10. Both may change before general availability (2026-07-20).
#
# Prerequisites:
#   * gh CLI authenticated as a user/admin who can configure the target repos
#     (gh auth login). The token needs the `repo` scope.
#   * Code Quality must be allowed for the org/enterprise that owns the repos.
#   * GitHub Actions must be enabled on each repo (Code Quality runs on Actions).
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

# Languages to analyze. Valid values (CodeQL-supported for Code Quality):
#   csharp, go, java-kotlin, javascript-typescript, python, ruby
LANGUAGES='["python","javascript-typescript"]'

if [[ ! -f "$CSV_FILE" ]]; then
  echo "❌ CSV file not found: $CSV_FILE" >&2
  exit 1
fi

echo "Enabling Code Quality for repositories listed in: $CSV_FILE"
echo

# Skip the header row, ignore blank lines.
tail -n +2 "$CSV_FILE" | tr -d '\r' | while IFS= read -r repo; do
  [[ -z "$repo" ]] && continue

  echo "→ $repo"
  if gh api \
      --method PATCH \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: ${API_VERSION}" \
      "/repos/${repo}/code-quality/setup" \
      -f "state=configured" \
      -f "languages[]=python" \
      -f "languages[]=javascript-typescript" \
      >/dev/null 2>&1; then
    echo "   ✅ Code Quality enablement requested"
  else
    echo "   ⚠️  Failed (check that the repo exists, Actions is enabled, and"
    echo "       Code Quality is allowed for the owning org/enterprise)"
  fi
done

echo
echo "Done. Re-run with a different CSV to target another set of repositories."
echo "Tip: confirm a single repo's status with:"
echo "  gh api -H \"X-GitHub-Api-Version: ${API_VERSION}\" /repos/OWNER/REPO/code-quality/setup"
