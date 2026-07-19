# T-SHIP-8 — apply lab doc sync (COMMIT half, forward-registered)
**Pack:** ship · **Status row:** `ship_tasks/SHIP_PROGRESS.md` · **Blocked by:** T-SHIP-7
**Lane:** coder · **Write scope:** exactly the category-A files listed in
`reports/DOC_DRIFT_2026-07-08.md` (+ progress note). Docs only — no source/test/corpus/
rule/yardstick file, no wiki domain fact, no `Vault/`, no dated/historical doc.

## Spec (final scope pinned after T-SHIP-7 lands)
Apply the A fix list verbatim: each edit's target text comes from the audit report, not
from re-research. If, mid-edit, a claim turns out to be a domain fact after all — STOP,
reclassify as B, surface. Category B items are owner decisions and stay untouched.

## Success criteria (provisional)
- `git status` delta == the A-list files + note, nothing else; diff per file matches the
  audit's "correct text" column.
- Full suite spot-check unchanged (docs cannot move tests — prove it: scoreboard
  `Hash lock: ok`, 269/294, split 191/78; one representative suite green).
- Both gate blocks; NO git commit — owner commits by explicit path (D-SHIP-4 lesson).
