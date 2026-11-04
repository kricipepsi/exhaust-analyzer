# T-AUD-7c — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. F-D3-2 and F-D3-3 (`audit/reports/R1_D3_20261017.md:28-46`): the anchors are unchanged on `6ce31ba` (`sed -n`).
   The done states are in the source ledgers (gaslab :52, registry :40, GRAPH_TRUST :14); the guard is 73.
2. The probe `audit/scratch/D3/ledgers.py` crashes on cp1252 when it writes `out/` (`→`): `PYTHONUTF8=1`. It rewrites
   the tracked `out/` files: restore after each run. Its summary goes to stdout, not `out/ledgers_summary.txt`.
3. Rehearsal (`make_rh.py` on the repo, then `git checkout --`): `pending` 5 → 1; both ledgers `(no pending row)`;
   3 claims `:NOT-FOUND`; no `FAIL` on the two ledgers; 3 files, 6+/6-.

### Rulings and the tradeoff that lost ###
- Flip the rows to `done` with the pointer to the done source. Lost: deleting the mirror rows (they record the DEP
  links other ledgers cite).
- Scope F-D3-2/3 only. Lost: `CLAUDE.md:65` and `ROADMAP.md:70` (F-D3 items with their own wording questions).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | `53`; `'pending': 1`; the two `(no pending row)` lines |
| step 2 | REHEARSED | `3`, `0` |
| step 3 | REHEARSED (diff stat) / DEFERRED (commit) | `3 files changed, 6 insertions(+), 6 deletions(-)` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-VINA-15` (`6ce31ba`).

### Progress hook ###
T-AUD-7c: COMLab, registry and vault-live ledgers offer no finished task as pending (F-D3-2, F-D3-3).

### Cold read ###
cold read: not triggered (docs row; rulings are verbatim old/new text, rehearsed end to end).

### Correction history ###
