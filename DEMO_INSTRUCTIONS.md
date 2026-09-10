# Code Quality Demo — Facilitator Instructions

A step-by-step script for demoing **GitHub Code Quality** end to end using the
**Cosmic Pizza** sample app.

> [!IMPORTANT]
> **Cost**
> 
> GitHub Code Quality is a paid product (~$10 / active committer / month on
> enabled repos, plus usage-based billing for AI-powered capabilities). CodeQL
> scans also consume **GitHub Actions minutes**. For product details, see:
> <https://docs.github.com/code-security/concepts/about-code-quality>
>
> **Where Code Quality runs**
> 
> Code Quality is available for **organization-owned repositories** on **GitHub
> Team** and **GitHub Enterprise Cloud**. It is **not** on GitHub Enterprise
> Server, and not on personal accounts. Make your demo copy inside a qualifying
> **organization**.
>
> **Supported languages (CodeQL / "Standard findings")**
>
> C#, Go, Java, JavaScript, Python, Ruby, TypeScript. This sample app is **Python**.
> A separate **AI-powered analysis** ("AI findings") looks at recently pushed
> files on the default branch and can flag issues in other languages too.

---

## At a glance

| Module | Theme | Time |
| --- | --- | --- |
| 0 | Before the training (setup) | 10 min |
| 1 | Enablement & configuration | 7 min |
| 2 | Review findings & fix them | 5 min |
| 3 | Pull request workflow | 12 min |
| 4 | Organization insights | 2 min |

---

## Module 0 — Before the training

Do this **ahead of time**, not live.

### 0.1 Create a copy from the template

1. Open the template repository on GitHub.
2. Click **Use this template ▸ Create a new repository**.
3. Choose an **organization** that is on **GitHub Team or Enterprise Cloud** (see
   the "Where Code Quality runs" note above) as the owner.
4. Name it something like `cosmic-pizza-demo`, set visibility to **Private**, and
   click **Create repository**.

> [!TIP]
> Create a **fresh copy for each delivery**. Several steps open pull requests
> and leave findings behind; a clean repo keeps the demo crisp.

### 0.2 Allow the workflow to open pull requests

Module 3 runs an Actions workflow that **creates a pull request**. By default
the built-in `GITHUB_TOKEN` is not allowed to open PRs, so enable it now:

1. In your new repo, go to **Settings ▸ Actions ▸ General**.
2. Scroll to **Workflow permissions**.
3. Select **Read and write permissions**.
4. Check **Allow GitHub Actions to create and approve pull requests**.
5. Click **Save**.

> [!NOTE]
> No secrets are required — the workflow uses the built-in `GITHUB_TOKEN`. The
> only thing you must flip is the setting above. (If your org enforces this at
> the **org** level under **Settings ▸ Actions ▸ General**, set it there instead.)

> [!IMPORTANT]
> **If these toggles are greyed out, the policy is set one level up.** Both
> **Actions permissions** and **"Allow GitHub Actions to create and approve pull
> requests"** can be controlled at the **org** *or* **enterprise** level. If they
> are locked/greyed at the repo level, you can't change them here — an **org owner
> or enterprise owner** has to allow them one level up (**org/enterprise Settings
> ▸ Actions ▸ General**), or you'll need to run the demo in an **org where these
> are already allowed**.

### 0.3 Confirm Actions is enabled

Code Quality runs CodeQL **on GitHub Actions**, so Actions must be on for the
repo. **Settings ▸ Actions ▸ General ▸ Actions permissions ▸ Allow all actions**
(or your org's policy equivalent). As with the pull-request permission above, if
this is greyed out it's being enforced at the **org or enterprise** level and
must be changed there first.

### 0.4 (If you belong to an enterprise) Confirm Code Quality is allowed

If your org is part of an enterprise, an enterprise owner must have **allowed
Code Quality**. If you can't see the **Code quality** setting in Module 1, this
is usually why. See:
<https://docs.github.com/code-security/how-tos/secure-at-scale/configure-enterprise-security/configure-specific-tools/allow-github-code-quality-in-enterprise>

### 0.5 Seed a few other repos so Module 4 lands

Module 4 shows the **organization-level** dashboard, which aggregates **every
Code Quality-enabled repo in the org**. A fresh org that only contains
`cosmic-pizza-demo` shows a **single bubble** and an almost-empty chart. Ahead of
the session, enable Code Quality on a handful of other repos so the bubble chart
and table actually tell a story — the enablement script
([`scripts/enable-code-quality.sh`](scripts/enable-code-quality.sh), Module 1.5)
is perfect for this.

> [!IMPORTANT]
> Enablement is **asynchronous**: the dashboard only fills in after each repo's
> first scan completes. Do this **well ahead of time**, not the morning of.

✅ **You're ready when:** the repo exists in a qualifying org, "Allow GitHub
Actions to create and approve pull requests" is checked, and Actions is enabled.

---

## Module 1 — Enablement & configuration

### 1.1 Enable Code Quality on the repository

1. In the repo, go to **Settings**.
2. In the left sidebar, under **Security**, click **Code quality**.
3. Click **Enable code quality**.

> [!TIP]
> Enabling kicks off the first CodeQL scan of the default branch. It runs as a
> **"Code Quality"** workflow on the **Actions** tab and takes a few minutes.
> Start it now so findings are ready for Module 2. (Talk track tip: while it
> runs, walk through the app and the intentional issues.)

### 1.2 Turn on AI findings

Code Quality ships two kinds of analysis: deterministic **CodeQL** results
("Standard findings") and **AI findings**. AI findings are off by default, so
turn them on now — you'll review them in **Module 2.2**.

1. Stay on **Settings** ▸ **Code quality**.
2. Under **Code Quality analysis**, find the **AI findings** setting —
   *"Generate AI-powered findings for code quality issues on push to the default
   branch."*
3. Flip the toggle from **Off** to **On**.

> [!TIP]
> AI findings are generated on **push to the default branch** and scan the
> **most recently changed files** — in any language, not just the ones CodeQL
> supports. The **Languages** checkboxes below the toggle only control the full
> CodeQL scan of the codebase.

### 1.3 Set up code coverage

Code Quality can show **code coverage** on pull requests. To enable it, add a
workflow that runs the tests, produces a **Cobertura XML** report, and uploads it
with the **`actions/upload-code-coverage@v1`** action (which needs the
**`code-quality: write`** permission).

This is the **setup** step — you create the workflow now. The coverage results
themselves show up on a pull request in **Module 3**.

Create `.github/workflows/code-coverage.yml` in your demo repo with the
following contents (commit it to `main`):

```yaml
name: Code Coverage

# Runs the test suite, produces a Cobertura XML coverage report, and uploads it
# to GitHub Code Quality. Once Code Quality is enabled for the repo, a coverage
# summary from github-code-quality[bot] appears on every pull request.
#
# Uploading requires the `code-quality: write` permission below.

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  code-quality: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      # Check out the PR head commit (not the merge commit) so coverage line
      # numbers map correctly to the diff.
      - uses: actions/checkout@v7
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}

      - uses: actions/setup-python@v6
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: pytest --cov=pizzeria --cov-report=xml

      - name: Upload coverage report
        if: github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository
        uses: actions/upload-code-coverage@v1
        with:
          file: coverage.xml
          language: Python
          label: code-coverage/pytest
          # Until Code Quality is enabled the upload endpoint returns 404. Treat
          # that as a warning so the workflow stays green out of the box; once
          # Code Quality is on, the upload succeeds and coverage shows up on
          # pull requests.
          fail-on-error: false
```

Then in **Module 3** you'll see the coverage results land on the PR as a comment
from **`github-code-quality[bot]`** comparing the PR branch's coverage to `main`.

> [!NOTE]
> Code coverage in pull requests works with **any language** that can emit a
> Cobertura XML report — this app uses `pytest --cov`.

### 1.4 Show how you can enable Code Quality at the org level

You don't have to enable repo by repo. To turn it on across all (or a subset of) repos in an
org at once:

1. Go to the **organization's** **Settings**.
2. In the sidebar, under **Security**, click **Code quality**.
3. Next to **Repository access**, click the drop-down to select one of the options:

<img width="1041" height="390" alt="Organization Code Quality settings showing the Repository access dropdown options" src="https://github.com/user-attachments/assets/f29d374a-b383-4b07-a51d-bcb2a2bfdf44" />

### 1.5 Show the enablement API for automation use cases

When you want Code Quality enabled as part of an automated process,
consider using the **[Code Quality setup API](https://docs.github.com/rest/code-quality/code-quality)**:

```
PATCH /repos/{owner}/{repo}/code-quality/setup
```

This repo ships a ready-to-run example script at
[`scripts/enable-code-quality.sh`](scripts/enable-code-quality.sh) that reads a
[`scripts/repos.csv`](scripts/repos.csv) file and, for each repo, **detects the
languages it uses** and enables Code Quality for the supported ones with the
`gh` CLI:

```bash
# 1) List the target repos (owner/repo), one per line, under the header:
cat scripts/repos.csv
# repository
# my-org/service-a
# my-org/service-b

# 2) Authenticate gh as someone who can configure those repos:
gh auth login            # token needs the `repo` scope

# 3) Enable Code Quality across the list:
./scripts/enable-code-quality.sh scripts/repos.csv

# ...or, if some repos have Actions turned off, also enable Actions in the same
#    pass (best effort — org/enterprise policy may still block it):
./scripts/enable-code-quality.sh --enable-actions scripts/repos.csv
```

For each repo the script first **checks whether Actions is enabled** (Code
Quality scans run on Actions) and warns if it is off. With `--enable-actions` it
also tries to turn Actions on, reporting a clear error if org/enterprise policy
prevents it. Then it asks GitHub which languages the
repo uses, keeps the ones Code Quality supports (`csharp`, `go`, `java-kotlin`,
`javascript-typescript`, `python`, `ruby`), and then enables exactly those:

```bash
# Detect the repo's languages:
gh api /repos/OWNER/REPO/languages --jq 'keys[]'
# -> Python
#    JavaScript

# Enable Code Quality for the supported, detected languages:
gh api --method PATCH \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  /repos/OWNER/REPO/code-quality/setup \
  -f state=configured \
  -f 'languages[]=python' \
  -f 'languages[]=javascript-typescript'
```

✅ **Module 1 done when:** the repo shows Code Quality enabled with **AI
findings** turned on, and the first scan has finished on the **Actions** tab.

---

## Module 2 — Review findings

By now the first default-branch scan has completed.

### 2.1 Review standard (CodeQL) findings

1. Open the **Security and quality** tab (the shield icon) in the repo.
2. In the sidebar, open **Standard findings** (this is the CodeQL rule-based
   analysis).
3. Walk through what the baseline app surfaces across a few files. For example:
   * **Maintainability** — an **unused import** and an **unused local variable**
     in `pizzeria/pricing.py`, another **unused import** and a block of
     **unreachable code** (after a `return`) in `pizzeria/orders.py`.
   * **Reliability** — a **duplicate key in a dict literal** in
     `pizzeria/menu.py` and an **`is` comparison with a string literal** in
     `pizzeria/orders.py`.

   For each finding:
   * Show the **rule**, the **category** (maintainability vs reliability), and the
     **severity**.
   * Open the finding to see the highlighted code and the explanation.

### 2.2 Review AI findings

1. In the same tab, switch to **AI findings** (you turned this on in
   **Module 1.2**).
2. Explain the difference: this is GitHub's **AI-powered analysis** of files
   **recently pushed to the default branch** (not the whole codebase), shown on a
   separate dashboard, and it can surface issues beyond the CodeQL-supported
   languages.

> [!NOTE]
> AI findings are presented separately from the deterministic CodeQL "Standard
> findings."

### 2.3 Assign up to 25 findings to Copilot with Agentic Autofix

1. Return to the **Standard findings** list and select one of the findings types. Then, select several instances of that finding. You can
   select and remediate **up to 25 findings at once**.
2. Click **Assign to Copilot**. This same Agentic Autofix flow works whether you
   select one finding or 25, replacing the previous one-at-a-time **Generate
   fix** action.
3. Explain that Copilot works autonomously on a branch, validates its changes by
   rerunning CodeQL, and opens a pull request for review.

> [!NOTE]
> Agentic Autofix is in **public preview** and consumes **Copilot AI credits**.
> Always review the generated changes before merging them.

### 2.4 Review the Agentic Autofix PR

1. Wait for Copilot to open a PR that addresses the selected findings.
2. Show the PR's changed files and validation results, then mention that you will
   take a closer look at the pull request workflow in the next module.

✅ **Module 2 done when:** you've shown Standard + AI findings, generated an
Agentic Autofix PR for multiple findings, and reviewed Copilot's changes.

---

## Module 3 — Pull request workflow

This is the headline demo: a PR that introduces fresh problems and shows
**CodeQL** reacting in the PR.

### 3.1 Run the workflow to create a "bad code" PR

1. Go to the **Actions** tab.
2. In the left list, choose **Introduce code quality issues**.
3. Click **Run workflow** (optionally tweak the PR title) ▸ **Run workflow**.
4. Wait ~30–60s. The workflow creates a branch, adds `pizzeria/promo.py`, and
   opens a pull request titled **"Add loyalty promo feature."**

> [!NOTE]
> **What it injects (so you know what to point at):**
>
> | Issue | Where | Caught by |
> | --- | --- | --- |
> | Unused local variable (`unused_tax`) | `apply_discount()` | CodeQL — maintainability |
> | Comparison of identical values (`subtotal == subtotal`) | `apply_discount()` | CodeQL — reliability |

### 3.2 Review the CodeQL findings on the PR

1. Open the new pull request (from the **Pull requests** tab). The **Code
   Quality** and **Code Coverage** workflows come back as **"action required"**
   and won't run until you approve them — scroll to the bottom of the PR and
   click **Approve and run** on the pending workflows. If you skip this, the
   CodeQL findings and coverage (Module 3.3) never appear and it looks broken.
2. Wait for the **Code Quality** check to run. The **`github-code-quality[bot]`**
   posts **inline comments** on `promo.py` for the CodeQL findings (unused
   variable, identical comparison).
3. Open the **Files changed** tab to read each inline finding and its
   explanation.

### 3.3 Review the code coverage results

1. Note that the code coverage results show both the stats for the
   target branch and the head branch, with a breakdown per file.

### 3.4 Dismiss a finding

1. Pick one finding you want to wave off (e.g. treat the identical-comparison as
   intentional for the demo).
2. Use the finding's **Dismiss finding** control and choose a reason (e.g.
   *Won't fix* / *Used in tests* / *False positive*).
3. Show that the dismissed finding drops out of the active list — useful for
   triaging noise.

### 3.5 Generate Copilot Autofix suggestions

1. On one of the remaining CodeQL findings (e.g. the **unused variable**), open
   the finding's autofix. Depending on where you're looking you'll see it as
   **Apply suggestion** (the inline autofix on the finding) or, from the
   finding's dropdown menu, **Fix with Copilot**.
2. Show the suggested diff that resolves the issue.

### 3.6 Add multiple fixes to a batch

1. Navigate to the **Files changed** tab and click on the Code Quality Bot icon
   to view its comments in line.
2. Where multiple findings each have an autofix, use **Add suggestion to batch**
   on each one instead of committing them one at a time.
3. Commit the batch as a single set of changes and show the PR updating, the
   checks re-running, and the findings clearing.

### 3.7 Quality gates with rulesets

Mention that **rulesets** can enforce quality gates on pull requests — blocking
merges that don't meet **maintainability**, **reliability**, or **coverage**
thresholds — so quality standards are enforced, not just reported.

1. Go to the repo's **Settings** tab.
2. Under the **Rules** drop down, select **Rulesets**.
3. Select **New ruleset**, then select **New branch ruleset**.
4. Review the general ruleset options: Enforcement status, Bypass list, Target branches.
5. Scroll down to the **Rules** section and check the **Require code quality results** checkbox.
6. Select the **Severity** dropdown that appears and highlight the options.
7. Still in the **Rules** section, also check the **Restrict code coverage**
   checkbox. In addition to requiring code quality results, this
   enforces specific **code coverage thresholds** that must be met before a PR
   can be merged.
8. Expand **Show additional settings** and set the two thresholds:
   * **Minimum coverage percentage** — the absolute floor (e.g. `60`). Pull
     requests with coverage below this threshold are blocked.
   * **Maximum coverage drop** — how many percentage points coverage may drop
     relative to the default branch (e.g. `20`). Pull requests that reduce
     coverage by more than this amount are blocked.

✅ **Module 3 done when:** you've shown CodeQL findings on one PR, dismissed
one, autofixed one, batched multiple fixes, and reviewed enforcement via rulesets
(code quality **and** coverage).

---

## Module 4 — Organization insights

### 4.1 Open the org-level Code Quality overview

1. Go to the **organization's** main page.
2. Click the **Security and quality** tab (shield icon).
3. In the **Insights** section of the sidebar, click **Code quality**.

> [!NOTE]
> The dashboard only shows repositories where **you can see** the findings, so
> permissions are respected automatically (admins see everything; developers see
> what they have access to).

### 4.2 Emphasize the out-of-the-box insights

Walk through what teams get with **zero extra setup**:

* **Score distribution chart** — each bubble is a group of repos plotted by
  **maintainability** (vertical) and **reliability** (horizontal). Higher and
  further-right is healthier; **bubble size** = number of repos; **color/border**
  reflects the lower of the two scores (red dashed = "Needs improvement").
* **Repository table** — every repo with Code Quality enabled, sortable by
  **Standard findings**, score, last scan, etc. Sort by Standard findings to
  surface the noisiest repos; sort by last scan to focus on what changed.
* **Drill-down** — click a low-scoring bubble to filter the table, then click a
  repo name to jump into its **repository-level** dashboard.

> [!TIP]
> **Talk track:** this is how an engineering leader answers "where is our
> technical debt concentrated, and which repos should we tackle first?" — at a
> glance, without bespoke tooling.

✅ **Module 4 done when:** you've shown the org bubble chart + repo table and
explained how leaders prioritize remediation.

---

## Handy links

- About Code Quality: <https://docs.github.com/code-security/concepts/about-code-quality>
- Enable Code Quality: <https://docs.github.com/code-security/how-tos/maintain-quality-code/enable-code-quality>
- Code coverage setup: <https://docs.github.com/code-security/how-tos/maintain-quality-code/set-up-code-coverage>
- Code Quality REST API: <https://docs.github.com/rest/code-quality/code-quality>
- Org dashboard: <https://docs.github.com/code-security/how-tos/view-and-interpret-data/analyze-organization-data/explore-code-quality>
- GA announcement (Jul 20, 2026): <https://github.blog/changelog/2026-06-16-github-code-quality-generally-available-july-20-2026/>
