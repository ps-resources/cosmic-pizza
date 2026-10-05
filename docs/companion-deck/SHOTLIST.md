# Screenshot shot list

The deck uses eight screenshots from the Cosmic Pizza demo, taken after working
through Modules 0 to 4 of `DEMO_INSTRUCTIONS.md`. Raw captures go in
`assets/screens/unedited/` (git-ignored, because raw captures can show avatars
and account details). `scripts/process-screens.py` crops each one into the file
a slide uses:

```sh
python3 scripts/process-screens.py
```

The script needs Pillow. Crop boxes are listed at the top of the script, in the
coordinates of a 2000 px wide preview of the raw capture, so a retaken
screenshot only needs its raw file replaced and the script re-run.

## Capture tips

- Use GitHub's dark theme and capture the whole browser window.
- Hide anything personal: avatars, email addresses, tokens, notification dots.
  The crops already exclude the page header.

## Shots

| Shot | Slide | Raw files | Output | What it shows |
|---|---|---|---|---|
| 01 | 03 Enablement | `01.png` | `shot-01-enable-settings.png` | Settings › Code quality: analysis toggle, enabled banner, scan and workflow links |
| 02 | 05 Standard findings | `02a.png`, `02b.png` | `shot-02-standard-findings.gif` | Findings list with scores, then the detail of one finding |
| 03 | 06 AI findings | `03.png` | `shot-03-ai-findings.png` | The AI findings page |
| 04 | 07 Pull request feedback | `04.png` | `shot-04-pr-inline-findings.png` | The bot's inline comment with severity and explanation |
| 05 | 08 Coverage | `05.png` | `shot-05-pr-coverage-comment.png` | The Code Coverage Overview comment on a pull request |
| 06 | 09 Quality gates | `06a.png`, `06b.png` | `shot-06-ruleset-settings.gif` | Ruleset settings: severity dropdown, then coverage thresholds |
| 07 | 10 Dashboards | `07.png` | `shot-07-org-dashboard.png` | The organization score distribution chart |
| 08 | 11 Bulk remediation | `8a.png`, `8b.png` | `shot-08-assign-to-copilot.gif` | Findings selected with Assign to Copilot, then a suggested changeset |

Two-state shots are animated GIFs (2.4 seconds per state, looping). Each also
has a `.png` of the first state, for a static export.
