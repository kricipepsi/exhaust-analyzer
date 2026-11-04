# T-AUD-7g — authoring sidecar (Windows Cowork, 2026-11-05, scheduled session 4dapp-cowork-2)

### Verified context ###
1. F-D3-13, F-D3-17 (`audit/reports/R1_D3_20261017.md:130-137`, `:166-173`): on `b8e1f28`, `ledgers.py` section H
   finds all five claims and every ledger it cites says `done`; `rules.py` finds the X5 and X11 quotes.
2. `.agent/coders/` holds agy, claude, codex, deepseek, glm, nemo (`ls`).
3. Rehearsal (`make_rh.py` on the repo, then `git checkout --`): `sides not found` 18 → 21; section H 0 → 5
   `NOT-FOUND`; 3 files, 9+/8-.

### Rulings and the tradeoff that lost ###
- The gate cells say `done` and point at the ledger for the next row. Lost: naming each pack's next row (it goes
  stale again at the next acceptance, which is the defect).
- DECISIONS D3 is marked superseded in its own cell, with the old ruling kept. Lost: a new row (the log has no
  supersede convention; one cell keeps the history next to the change).
- `AGENTS.md:23` wins the wiki question: the live tree has `labs/gaslab/wiki/` and no `docs/GASLab/wikiNEW/`.
- F-D3-16 (follow-up IDs and statuses) is ledger cells only: Cowork's, not this row.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | `sides not found: 21`; `3` |
| step 2 | REHEARSED | `5` |
| step 3 | REHEARSED (diff stat) / DEFERRED (commit) | `3 files changed, 9 insertions(+), 8 deletions(-)` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-AUD-7f` (`b8e1f28`).

### Progress hook ###
T-AUD-7g: router and ROADMAP report the ledgers' states; six-identity roster; one canonical wiki (F-D3-13/17).

### Cold read ###
cold read: not triggered (docs row; rulings are verbatim old/new text, rehearsed end to end).

### Correction history ###
