# T-AUD-7d — authoring sidecar (Windows Cowork, 2026-11-05, scheduled session 4dapp-cowork-2)

### Verified context ###
1. F-D3-4, F-D3-6, F-D3-9 (`audit/reports/R1_D3_20261017.md:47-100`): the D3 probes re-run on `9de409b` find every
   quote (`recheck/T-AUD-7d/rules_base.out`, `led_base.out`). Line numbers moved after T-AUD-7a/b; the probe prints
   the current ones (`4DLab_CLAUDE.md:238`, not `:265`).
2. Section G of `ledgers.py` also lists `Codex + Agy + Claude → T-GTA-<lab>`; every row of
   `apps/vault/audit/GRAPH_TRUST_PROGRESS.md` is `done` (T-AUD-7c review), so R2 clears it.
3. PCT-9/10: `apps/wiredV2` does not exist; `apps/wired/wired/run_case.py:14` reads
   `apps/wired/tests/fixtures/oil_cases/` (`MW-001.json` … `MW-009.json`).
4. Rehearsal (`make_rh.py` on the repo, then `git checkout --`): `sides not found` 4 → 8; PCT blocker lines 18 → 0;
   section G empty; post-cat-trim `wiredv2` lines 3 → 0; 6 files, 37+/35-.
5. `primary status counts` from `ledgers.py` does not count the post-cat-trim ledger (unchanged 1 → 1), and the spec
   commit adds a `pending` audit row, so the gate does not use it.

### Rulings and the tradeoff that lost ###
- F-D3-4: the ledger wins over the assignment. `4DLab_CLAUDE.md:238` and the assignments file's own History (the
  2026-07-06 stale-pointer fix) both say an assignment drifts. Lost: the assignment wins (it keeps manager control,
  but it needs a flip after every task and it has drifted twice).
- F-D3-9: PCT-2..10 → `deferred`, PCT-1 stays `pending` (its spec is the START_HERE section; T-VIN-FIX-3 is done).
  Lost: deleting the chain (it is a planned effort the owner registered).
- F-D3-6: ROADMAP follows `AGENTS.md` rule 4. Lost: tightening AGENTS to "existing consumer" (rule 4 is the newer
  ruling and `4DLab_CLAUDE.md:50` agrees with it).
- Scope F-D3-4/6/9 only. Lost: one row for all of F-D3-4…9. F-D3-5 needs a graph-lane ruling across 8 documents, and
  F-D3-7/8 are a separate wording row (T-AUD-7e).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | 4 `NOT FOUND` lines; `sides not found: 8` |
| step 2 | REHEARSED | `0`, `0` |
| step 3 | REHEARSED | `0` |
| step 4 | REHEARSED (diff stat) / DEFERRED (commit) | `6 files changed, 37 insertions(+), 35 deletions(-)` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-AUD-7c` (`9de409b`).

### Progress hook ###
T-AUD-7d: the ledger wins over an assignment; ROADMAP consumer rule = AGENTS rule 4; PCT-2..10 deferred (F-D3-4/6/9).

### Cold read ###
cold read: not triggered (docs row; rulings are verbatim old/new text, rehearsed end to end).

### Correction history ###
