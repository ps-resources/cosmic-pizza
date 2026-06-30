# Code Quality Demo — Facilitator Instructions

A step-by-step script for demoing **GitHub Code Quality** end to end using the
**Cosmic Pizza** sample app.

> [!WARNING]
> **Preview notice — read me first**
> GitHub Code Quality is in **public preview** and becomes **generally available
> on July 20, 2026**. During the preview it is **free**, although CodeQL scans
> consume **GitHub Actions minutes**. After GA it is a paid product
> (~$10 / active committer / month on enabled repos, plus usage-based billing for
> AI-powered capabilities). Anything tagged **_(preview)_** below may change
> before GA, so re-check the docs the morning of your session:
> <https://docs.github.com/code-security/concepts/about-code-quality>

> [!IMPORTANT]
> **Where Code Quality runs**
> Code Quality is available for **organization-owned repositories** on **GitHub
> Team** and **GitHub Enterprise Cloud**. It is **not** on GitHub Enterprise
> Server, and not on personal accounts. Make your demo copy inside a qualifying
> **organization**.

> [!NOTE]
> **Supported languages (CodeQL / "Standard findings"):** C#, Go, Java,
> JavaScript, Python, Ruby, TypeScript. This sample app is **Python**.
> A separate **AI-powered analysis** ("AI findings") looks at recently pushed
> files on the default branch and can flag issues in other languages too.

---

## At a glance

| Module | Theme | Time |
| --- | --- | --- |
| 0 | Before the training (setup) | 10 min |
| 1 | Enablement & configuration | 10 min |
| 2 | Review findings & fix them | 10 min |
| 3 | Pull request workflow | 10 min |
| 4 | Organization insights | 5 min |

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

### 0.3 Confirm Actions is enabled

Code Quality runs CodeQL **on GitHub Actions**, so Actions must be on for the
repo. **Settings ▸ Actions ▸ General ▸ Actions permissions ▸ Allow all actions**
(or your org's policy equivalent).

### 0.4 (If you belong to an enterprise) Confirm Code Quality is allowed

If your org is part of an enterprise, an enterprise owner must have **allowed
Code Quality**. If you can't see the **Code quality** setting in Module 1, this
is usually why. See:
<https://docs.github.com/code-security/how-tos/secure-at-scale/configure-enterprise-security/configure-specific-tools/allow-github-code-quality-in-enterprise>

✅ **You're ready when:** the repo exists in a qualifying org, "Allow GitHub
Actions to create and approve pull requests" is checked, and Actions is enabled.

---

## Module 1 — Enablement & configuration

### 1.1 Enable Code Quality on the repository

1. In the repo, go to **Settings**.
2. In the left sidebar, under **Security**, click **Code quality**.
3. Click **Enable code quality**.
4. Review the configuration:
   * **Languages** — leave **Python** checked (uncheck any you don't want
     analyzed).
   * **Runner type** — leave **Standard** (GitHub-hosted) unless you need a
     labeled/self-hosted runner.
5. Click **Save changes**.

> [!TIP]
> Enabling kicks off the first CodeQL scan of the default branch. It runs as a
> **"Code Quality"** workflow on the **Actions** tab and takes a few minutes.
> Start it now so findings are ready for Module 2. (Talk track tip: while it
> runs, walk through the app and the intentional issues.)

### 1.2 Configure code coverage _(preview)_

This template already includes a coverage workflow
(`.github/workflows/code-coverage.yml`). It runs the tests, produces a
**Cobertura XML** report, and uploads it with the
**`actions/upload-code-coverage@v1`** action (which needs the
**`code-quality: write`** permission — already set in the workflow).

To show coverage on a PR:

1. Point out the workflow file and the `Upload coverage report` step.
2. Coverage results appear automatically on pull requests once Code Quality is
   enabled — you'll see them in Module 3 as a comment from
   **`github-code-quality[bot]`** comparing the PR branch's coverage to `main`.

> [!NOTE]
> **_(preview)_** Code coverage in pull requests is in public preview. It works
> with **any language** that can emit a Cobertura XML report — this app uses
> `pytest --cov`.

### 1.3 Show how you *could* enable Code Quality at the org level _(preview)_

You don't have to enable repo by repo. To turn it on for **every** repo in an
org at once:

1. Go to the **organization's** **Settings**.
2. In the sidebar, under **Security**, click **Code quality**.
3. Toggle **Enable Code Quality** on to apply it to all repositories.

> [!NOTE]
> **_(preview)_** Organization-level enablement is in public preview. Use it to
> roll Code Quality out broadly; use the API below when you want a curated subset.

### 1.4 Show the enablement API for "many, but not all" repos _(preview)_

When you want Code Quality on a **specific list** of repos (not the whole org),
script it with the **Code Quality setup API**:

```
PATCH /repos/{owner}/{repo}/code-quality/setup
```

This repo ships a ready-to-run example at
[`scripts/enable-code-quality.sh`](scripts/enable-code-quality.sh) that reads a
[`scripts/repos.csv`](scripts/repos.csv) file and enables each one with the
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
```

Under the hood each row becomes:

```bash
gh api --method PATCH \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  /repos/OWNER/REPO/code-quality/setup \
  -f state=configured \
  -f 'languages[]=python' \
  -f 'languages[]=javascript-typescript'
```

> [!NOTE]
> **_(preview)_** The Code Quality REST API uses the dated API version
> **`2026-03-10`** and may change before GA. You can confirm a repo's status with
> `GET /repos/{owner}/{repo}/code-quality/setup`.

✅ **Module 1 done when:** the repo shows Code Quality enabled and the first scan
has finished on the **Actions** tab.

---

## Module 2 — Review findings

By now the first default-branch scan has completed.

### 2.1 Review standard (CodeQL) findings

1. Open the **Security and quality** tab (the shield icon) in the repo.
2. In the sidebar, open **Standard findings** (this is the CodeQL rule-based
   analysis).
3. Walk through what the baseline app surfaces — for example an **unused import**
   and an **unused local variable** in `pizzeria/pricing.py`. For each finding:
   * Show the **rule**, the **category** (maintainability vs reliability), and the
     **severity**.
   * Open the finding to see the highlighted code and the explanation.

### 2.2 Review AI findings _(preview)_

1. In the same tab, switch to **AI findings**.
2. Explain the difference: this is GitHub's **AI-powered analysis** of files
   **recently pushed to the default branch** (not the whole codebase), shown on a
   separate dashboard, and it can surface issues beyond the CodeQL-supported
   languages.

> [!NOTE]
> **_(preview)_** AI findings are part of the preview and presented separately
> from the deterministic CodeQL "Standard findings."

### 2.3 Generate a fix

1. Open one of the Standard findings (e.g. the **unused import** in
   `pricing.py`).
2. Use the **Copilot Autofix** suggestion attached to the finding to generate a
   proposed fix.

> [!TIP]
> You **do not** need a Copilot or Code Security license to use Code Quality or
> apply Copilot-powered autofixes.

### 2.4 Open a PR with the fixes

1. Accept the generated fix(es) and let GitHub **create a pull request** with the
   changes (or commit them to a new branch).
2. Note that opening this PR triggers a fresh Code Quality scan **on the PR** —
   leading nicely into Module 3.
3. You can merge this "cleanup" PR to show the finding being resolved.

✅ **Module 2 done when:** you've shown Standard + AI findings, generated an
autofix, and opened a fix PR.

---

## Module 3 — Pull request workflow

This is the headline demo: a PR that introduces fresh problems and shows both
**CodeQL** and **Copilot Code Review (CCR)** reacting in the PR.

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
> | Mutable default argument (`history=[]`) | `apply_discount()` | Copilot Code Review |
> | O(n²) loop | `frequency_bonus()` | Copilot Code Review |

### 3.2 Review the CodeQL findings on the PR

1. Open the new pull request (from the **Pull requests** tab).
2. Wait for the **Code Quality** check to run. The **`github-code-quality[bot]`**
   posts **inline comments** on `promo.py` for the CodeQL findings (unused
   variable, identical comparison).
3. Open the **Files changed** tab to read each inline finding and its
   explanation.

### 3.3 Review the Copilot Code Review findings

1. If Copilot Code Review isn't already running on PRs, request it: in the PR,
   open **Reviewers** and request a review from **Copilot** (or rely on your org's
   automatic CCR rule if configured).
2. Copilot Code Review posts its own comments — point out the **performance**
   (O(n²) loop) and the **mutable default argument** call-outs. Contrast this with
   CodeQL: CCR blends an LLM with deterministic tools for context-aware feedback.

> [!NOTE]
> **_(preview)_** Copilot Code Review's newest capabilities (deterministic
> detections, agentic fix hand-off) are in public preview and may change.

### 3.4 Dismiss a finding

1. Pick one finding you want to wave off (e.g. treat the identical-comparison as
   intentional for the demo).
2. Use the finding's **⋯ / Dismiss** control and choose a reason (e.g. *Won't
   fix* / *Used in tests* / *False positive*).
3. Show that the dismissed finding drops out of the active list — useful for
   triaging noise.

### 3.5 Generate an Autofix for a finding

1. On one of the remaining CodeQL findings (e.g. the **unused variable**), open
   the **Copilot Autofix** suggestion.
2. Show the suggested diff that removes the dead code.

### 3.6 Add multiple fixes to a batch

1. Where multiple findings each have an autofix, **add them to a batch** instead
   of committing one at a time.
2. Commit the batch as a single set of changes and show the PR updating, the
   checks re-running, and the findings clearing.

> [!TIP]
> Optional flex: assign remediation to the **Copilot coding agent** (requires a
> Copilot license) to have it open a follow-up fix PR for you.

✅ **Module 3 done when:** you've shown CodeQL + CCR findings on one PR, dismissed
one, autofixed one, and batched multiple fixes.

---

## Module 4 — Organization insights _(preview)_

> [!NOTE]
> **_(preview)_** The organization-level Code Quality dashboard is in public
> preview.

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

### 4.3 (Optional) Quality gates with rulesets _(preview)_

Mention that **rulesets** can enforce quality gates on pull requests — blocking
merges that don't meet **maintainability**, **reliability**, or **coverage**
thresholds — so quality standards are enforced, not just reported.

✅ **Module 4 done when:** you've shown the org bubble chart + repo table and
explained how leaders prioritize remediation.

---

## Reset / re-run checklist

- Delete branches/PRs created by the **Introduce code quality issues** workflow
  (named `demo/loyalty-promo-*`) and the fix PR from Module 2.
- Or simplest: spin up a **fresh template copy** per delivery (Module 0).

## Handy links

- About Code Quality: <https://docs.github.com/code-security/concepts/about-code-quality>
- Enable Code Quality: <https://docs.github.com/code-security/how-tos/maintain-quality-code/enable-code-quality>
- Code coverage setup: <https://docs.github.com/code-security/how-tos/maintain-quality-code/set-up-code-coverage>
- Code Quality REST API: <https://docs.github.com/rest/code-quality/code-quality>
- Org dashboard: <https://docs.github.com/code-security/how-tos/view-and-interpret-data/analyze-organization-data/explore-code-quality>
- GA announcement (Jul 20, 2026): <https://github.blog/changelog/2026-06-16-github-code-quality-generally-available-july-20-2026/>
