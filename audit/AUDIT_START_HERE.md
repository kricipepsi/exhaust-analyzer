# AUDIT_START_HERE — 4DLab audit venue (round 1, opened 2026-10-17)

Goal: find defects in 4DLab code and documents by falsification, prove each one, and turn the proven ones
into task rows. The venue changes no source; fixes go through the normal task workflow (`CLAUDE.md`).

## Roles
- **Architect (Cowork):** ranks targets, starts sessions, re-checks every finding, owns `FINDINGS.md`, authors
  fix rows. Decides everything except keyboard actions (`CLAUDE.md` §Operator interaction).
- **Auditor:** one session, one target, contract `AUDITOR.md`, prompt from `PROMPTS.md`. Writes only its report.
- **Operator:** the keyboard actions listed under §Operator actions, nothing else.

## Files
| file | what |
|---|---|
| `AUDITOR.md` | the auditor contract: falsification method, finding format, report shape |
| `PROMPTS.md` | one prompt per target, in run order |
| `FINDINGS.md` | the ledger: every finding, its re-check verdict and its owner row |
| `FIX_PLAN.md` | findings grouped into fix rows T-AUD-1…10, priority and rulings |
| `reports/` | auditor reports, `R0_baseline_20261017.md`, `baseline_*.txt` |
| `tools/setup.sh`, `tools/baseline.sh` | Python 3.14 audit venv; per-package pytest + erosion + isolation |
| `tools/erosion.py`, `tools/isolation.py` | SlopCodeBench-style erosion census; lab-isolation import scan |
| `scratch/<target>/` | auditors' probe tests and scripts (evidence, never product code); each finding's probe is its fix row's acceptance test |

## Rounds
| round | targets | where | status |
|---|---|---|---|
| R0 | secrets, test baseline, erosion, isolation | architect | **done** — `reports/R0_baseline_20261017.md` |
| R1 | C1, C4, C2, D1, D3, C3, C5, C6, D2 | 9 read-only subagents of the architect session (2026-10-17) | **done** — 161 findings UPHELD by probe/script re-run (42 HIGH, 88 MEDIUM, 34 LOW incl. R0; 3 duplicates merged); `FIX_PLAN.md` |
| R2 | re-attack each target after its fix rows land | same | later |

How sessions run: preferred is a cloud session per target at claude.ai/code on `kricipepsi/exhaust-analyzer`
(the repo is public; nothing secret is needed once R0-1 is fixed). The architect may run the same prompts as
read-only subagents instead. Up to three targets run in parallel; they touch no shared file.

## Re-check (the only way a finding enters the ledger)
1. Run the finding's `repro` on the **live working tree**, not on the report's copy.
2. It reproduces → `UPHELD`, and the architect names an owner row (new task spec or an existing row).
   It does not → `NOT REPRODUCED`, with the command. It cannot be run → `UNVERIFIED`; it never becomes a task.
3. Nothing is fixed from a report's prose. A HIGH in a lab stops new task assignment in that lab until its row
   is authored.

## Operator actions (keyboard only)
1. Push the venue commits to `exhaust-analyzer` `main` (this cloud session can read the repo but not push).
2. Start each cloud session the architect names, with the prompt the architect gives, and paste the final
   report back (or let the session push it to its branch). Not needed when the architect runs the targets
   as subagents.
(R0-1 key rotation: declined by the operator 2026-10-17, see `FINDINGS.md`.)

## Source of truth (architect ruling, 2026-10-17)
| tree | state | role in the audit |
|---|---|---|
| `github.com/kricipepsi/exhaust-analyzer` `main` @ `8463d21` | 2026-07-19, "4DLabV2 published build" | **audited tree** (newest known 4DLab) |
| `C:\Workspace` (Windows) git `master` @ `c5034a3` | 2026-06-26, last commit before the Linux migration, no remote; plus untracked `ECO/` (worked to 2026-08-25) | stale 4DLab copy, not audited. `ECO/` is a separate app outside this venue |
| `github.com/kricipepsi/4Dapp` `main` @ `490b82e` | 2026-05-11, v1 (`v1.0-diesel` tag 2026-05-12) | predecessor; legacy v1 is not truth (AGENTS.md rule 2), not audited |
Lost alternative: auditing `C:\Workspace` because it is the operator's current PC; rejected because its 4DLab code is 23 days older than `main`.

## Deployment coupling (architect ruling, 2026-10-17)
- `render.yaml` deploys `main` to Render (`4d-diagnostic-engine-v2`, Streamlit `app.py`), served at
  https://www.5-gasanalyzermot.com/. **Every push to `main` redeploys the public app.**
- https://5gasdiagnostic.com/ is the landing site (LiteSpeed host, not GitHub Pages) and links to the app. Its
  source location is not in this repo.
- Rule: audit-venue commits (only `audit/`, docs, `.gitignore`) may go to `main`. Every fix row lands on a branch,
  passes its gates and the affected lab suites, then merges to `main`; after the merge the architect checks the live
  app still loads and, if the change alters what the landing site states, opens a landing-site row.
  Lost alternative: fix rows straight to `main`, rejected because `main` is production.
