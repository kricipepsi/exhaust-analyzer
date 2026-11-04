# T-AUD-7f — authoring sidecar (Windows Cowork, 2026-11-05, scheduled session 4dapp-cowork-2)

### Verified context ###
1. F-D3-5 (`audit/reports/R1_D3_20261017.md:56-63`): `rules.py` on `2e78315` finds every X2 and X3 quote
   (`recheck/T-AUD-7f/rules_base.out`); `ledgers.py` A2 lists T-GR-11 with the pending blocker T-GR-10.
2. The pack's status vocabulary (`GRAPH_ROLLOUT_PROGRESS.md`, "Status values") has `blocked`, not `deferred`;
   `AGENTS.md` rule 3 skips both. Cowork set T-GR-11 `blocked` (`41ccddd`); A2 then lists no T-GR row.
3. Rehearsal (`make_rh.py` on the repo, then `git checkout --`): `sides not found` 14 → 18 (4 in X2/X3);
   `T-GR-10/11` in AGENTS 0 → 1, pack START_HERE 2 → 3; 7 files, 11+/8-.

### Rulings and the tradeoff that lost ###
- One lane rule: builds are architect-lane; the owner's T-GR-10/11 `extract` is the one Nemo exception; coders query.
  It restates the two 2026-07-06 owner rulings and reverses neither. Lost: architect-only with no exception (it would
  overturn the owner's pack amendment, which is the operator's call).
- "Frozen" means frozen for coders; an architect-lane row (T-GR-9) may refresh a tier. Lost: frozen for everyone
  (T-GR-9 is done and accepted by the owner, so the rule would contradict the record).
- T-GR-10 stays `pending`: its owner hold date passed and its spec exists. Whether Nemo runs it is the owner's choice.
- The harness git line (F-R3-5 residue, found in T-AUD-7e) joins this row. Lost: a separate one-line row.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | `sides not found: 18`; `4` |
| step 2 | REHEARSED | `AGENTS.md:1`, `…START_HERE.md:3`; `1`; `0` |
| step 3 | REHEARSED (diff stat) / DEFERRED (commit) | `7 files changed, 11 insertions(+), 8 deletions(-)` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-AUD-7e` (`2e78315`) and Cowork's ledger commit `41ccddd`.

### Progress hook ###
T-AUD-7f: one graph-build lane rule (architect; T-GR-10/11 Nemo extract the one exception); harness git line (F-D3-5).

### Cold read ###
cold read: not triggered (docs row; rulings are verbatim old/new text, rehearsed end to end).

### Correction history ###
