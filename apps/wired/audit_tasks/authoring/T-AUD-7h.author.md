# T-AUD-7h — authoring sidecar (Windows Cowork, 2026-11-05, scheduled session 4dapp-cowork-2)

### Verified context ###
1. R0-3 (`audit/FINDINGS.md:13`): ADR-0002 is Accepted (`labs/dnalab/docs/ADR_DNALab.md:15`); `labs/dnalab/dnalab`
   has 5 top-level `vinlab`/`symptomlab` imports (`grep`).
2. F-D3-18: `rules.py` X10 finds every quote on `0fdf971`; no Vault pack has a `pending` row (report :179).
3. Rehearsal (`make_rh.py` on the repo, then `git checkout --`): `sides not found` 21 → 22; the 4 `4DLab_CLAUDE.md`
   `wiredV2`/`Vault/tasks` path lines → 1 (`:178`); 2 files, 6+/5-.

### Rulings and the tradeoff that lost ###
- R0-3: the rule names the ADR exception. Lost: removing the imports (ADR-0002 is an Accepted design decision, and the
  code follows it; a code change is a T-AUD-2-class row, not docs).
- F-D3-18: retire the Vault packs from the bootstrap table; "Never edit `Vault/`" stays absolute. Lost: an
  AGENTS.md exception for Vault ledger flips (no Vault row is `pending`, so the exception would serve no work).
- F-D3-19 takes only the wiredV2 bootstrap row here; the 99 MISSING paths are a separate survey.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | `sides not found: 22`; `1` |
| step 2 | REHEARSED | `4DLab_CLAUDE.md:178`; `1` |
| step 3 | REHEARSED (diff stat) / DEFERRED (commit) | `2 files changed, 6 insertions(+), 5 deletions(-)` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-AUD-7g` (`0fdf971`).

### Progress hook ###
T-AUD-7h: AGENTS rule 5 names ADR-0002's import edge; Vault packs leave the bootstrap table; app row → apps/wired.

### Cold read ###
cold read: not triggered (docs row; rulings are verbatim old/new text, rehearsed end to end).

### Correction history ###
