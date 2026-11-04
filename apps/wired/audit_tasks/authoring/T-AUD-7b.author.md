# T-AUD-7b — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. F-R3-5 (CONFIRMED, MED) in `audit/reports/R3_verification_windows_20261104.md` on `audit-r3-verify` (`63af629`):
   four docs still say "never branch". Routed to the audit pack as the rest of FIX_PLAN T-AUD-7 (git rule), the same
   pack as T-AUD-7a.
2. Population measured on `fix/T-VINA-18` (`c9580f9`) with the R3 filter: "never branch" → 4 lines (P1); "only git
   action" → 6 files (P2). `v3/V3_PLAN.md:203` states the same stale rule without "never branch", so it is in scope.
   `planning/graph_rollout/LMM-gphfy.md:15` is a pasted chat transcript, not a rule: out of scope (R6).
3. All five files are LF (`git ls-files --eol`: `i/lf w/lf`; byte count CRLF 0).
4. `fix/T-AUD-7a` is an ancestor of `fix/T-VINA-18` (`git merge-base --is-ancestor`), so `4DLab_CLAUDE.md` §Git on
   the base already says "one branch per task".

### Rulings and the tradeoff that lost ###
- Align each line with `4DLab_CLAUDE.md` §Git and point at it. Lost: marking the docs superseded. The four docs are
  still entry points (START_HERE, INSTRUCTIONS, handoff), so a banner would leave the wrong rule in the text.
- Include `v3/V3_PLAN.md:203`. Lost: the R3 list only. The same rule in a fifth doc would survive the row.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | `0` |
| step 2 | REHEARSED | `./planning/graph_rollout/LMM-gphfy.md` only |
| step 3 | REHEARSED | `1` for each of the 5 files |
| step 4 | REHEARSED (diff stat, eol) / DEFERRED (commit) | `5 files changed, 9 insertions(+), 10 deletions(-)`; `5 i/lf w/lf`; restored with `git checkout -- .`, status clean |

Rehearsal script: `C:/4DApp/recheck/scratch/rehearse_7b.py` (asserts each old block occurs once).

### Exclusivity ###
No other implementer runs. Built on `fix/T-VINA-18` (`c9580f9`).

### Progress hook ###
T-AUD-7b: no filtered doc says "never branch"; 5 docs point at `4DLab_CLAUDE.md` §Git.

### Cold read ###
cold read: not triggered (docs row, difficulty 1; rulings are verbatim old/new blocks, rehearsed end to end).

### Correction history ###
