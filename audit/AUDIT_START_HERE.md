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
| `reports/` | auditor reports, `R0_baseline_20261017.md`, `baseline_*.txt` |
| `tools/setup.sh`, `tools/baseline.sh` | Python 3.14 audit venv; per-package pytest + erosion + isolation |
| `tools/erosion.py`, `tools/isolation.py` | SlopCodeBench-style erosion census; lab-isolation import scan |
| `scratch/<target>/` | auditors' probe tests (evidence, never product code) |

## Rounds
| round | targets | where | status |
|---|---|---|---|
| R0 | secrets, test baseline, erosion, isolation | architect | **done** — `reports/R0_baseline_20261017.md` |
| R1 | C1, C4, C2, D1, D3, C3, C5, C6, D2 (`PROMPTS.md` order) | cloud sessions on the GitHub repo, or subagents of an architect session | open |
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
1. Rotate the Firecrawl API key (R0-1), and put the new key in the local, now untracked,
   `_skills/firecrawl-web-scraping-search/API.md`.
2. Make GitHub `main` match the working tree (push), so auditors read current code (R0-5).
3. Start each cloud session the architect names, with the prompt the architect gives, and paste the final
   report back (or let the session push it to its branch).
