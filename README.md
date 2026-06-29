# Cosmic Pizza 🍕🚀

A tiny, deliberately imperfect Flask app used to **demo GitHub Code Quality**.

Build a pizza, pick your toppings, and get a price + calorie count. Under the
hood the code carries a few small quality and performance issues on purpose, so
you can watch **Code Quality (CodeQL)**, **code coverage**, and **Copilot Code
Review** light them up.

> 📋 **Facilitators:** follow [`DEMO_INSTRUCTIONS.md`](DEMO_INSTRUCTIONS.md) for
> a full, step-by-step walkthrough (Modules 0–4).

> 🧪 **Preview notice:** GitHub Code Quality is in **public preview** and becomes
> generally available on **July 20, 2026**. Features marked _(preview)_ in the
> demo instructions may change.

## What's in here

| Path | What it is |
| --- | --- |
| `app.py` | Flask routes (`/`, `/order`, `/menu.json`) |
| `pizzeria/` | Menu data, pricing, and order logic |
| `templates/`, `static/` | The web UI |
| `tests/` | Pytest suite (intentionally ~95% coverage) |
| `.github/workflows/code-coverage.yml` | Runs tests and uploads Cobertura coverage |
| `.github/workflows/introduce-quality-issues.yml` | On-demand workflow that opens a PR with bad code |
| `scripts/enable-code-quality.sh` + `repos.csv` | Enable Code Quality across many repos via API |
| `demo/promo.py.txt` | The "bad code" template the workflow injects |

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
# open http://127.0.0.1:5000
```

## Run the tests

```bash
pip install pytest pytest-cov
pytest --cov=pizzeria --cov-report=term-missing
```

## This is a template repository

Click **Use this template** to create your own copy to demo in. Code Quality
runs on **organization-owned** repositories on **GitHub Team** or **GitHub
Enterprise Cloud**, so create your copy inside such an organization.
