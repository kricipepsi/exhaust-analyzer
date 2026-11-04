# T-AUD-7g progress note

## Readiness
(a) Starting state matches: branch `fix/T-AUD-7g`, `HEAD~1` = `b8e1f28`, `git status --porcelain` empty; preconditions print `checked`.
(b) The probes fail for the intended reason: base `rules.py` prints `sides not found: 18`; base `ledgers.py` section H finds the 5 `CLAUDE.md`/`ROADMAP.md` stale claims (0 `NOT-FOUND` lines), so the claims are still present.
(c) Expected after R1-R8: `sides not found: 21` (P2), 3 matching X5/X11 lines, 5 `:NOT-FOUND` lines in section H; derived from the P2 pin and `rehearsal.diff` (9 insertions, 8 deletions).
(d) No contradiction: the edits are exact strings in `make_rh.py`; all three files are in `### Files to touch ###`.
(e) Deliverable: one `docs(T-AUD-7g):` commit with the eight `make_rh.py` edits to `CLAUDE.md`, `ROADMAP.md` and `DECISIONS.md`. Decisive check: `rules.py` prints `sides not found: 21` and `ledgers.py` section H prints 5 `:NOT-FOUND` lines.

## Assumptions worked past
- The commit has no `Co-Authored-By` trailer: `bash_guard` refused every commit command whose text held the trailer (AGENTS.md § git).

## VERIFICATION GATE
CLEAN. Step 1: `sides not found: 21`, then `3`. Step 2: `5`. Step 3: spec commit `ebf07bb`, then `fe5b8a7 docs(T-AUD-7g):`; stat `3 files changed, 9 insertions(+), 8 deletions(-)`; `git status --porcelain` lists only the note (the RESULT follows). Base was `sides not found: 18` and 0 `:NOT-FOUND` lines in section H. `audit/scratch/D3/out/` restored after each run.

## CODE REVIEW
CLEAN. Docs only. The diff matches `rehearsal.diff` (same 9/8 stat; edits made with the Edit tool). No other file touched.

## Time
phase | start | end | minutes | context at end
all | 2026-11-04T23:44:12Z | 2026-11-04T23:45:29Z | 1.3 | ABSENT
