# T-SHIP-6 — final full-suite verification before GitHub push (READ-ONLY disclose)
**Pack:** ship · **Status row:** `ship_tasks/SHIP_PROGRESS.md` · **Blocked by:** — (all prior ship tasks done)
**Lane:** coder · **Write scope:** ONE report `apps/wired/ship_tasks/reports/SHIP_FINAL_VERIFY_2026-07-08.md`
(+ progress note `ship_tasks/progress_notes/T-SHIP-6.md`). **No source, test, corpus, rule,
or yardstick file may change.** Any red is a named FINDING, never a fix in this task.

## Why
T-SHIP-1 proved the tree green on 2026-07-07 — **before** the UI landed. Since then
T-SHIP-UI-2 (`8e0d08b`) and T-SHIP-UI-3 (still **uncommitted** in the working tree:
`apps/ui/app.py`, `apps/ui/ui_payload.py`, `apps/ui/tests/test_ui.py`, ledger, note,
plus untracked root `pyrightconfig.json`) changed the app surface. This task is the last
gate: prove the FULL app — engine + labs + UI — green on the working tree exactly as the
owner will commit and push it. After this report the only remaining actions are the
owner's: commit by explicit path, then push (branch `task/t-com-vault`; merge/push is
owner-run per `4DLab_CLAUDE.md` — never suggested, never performed here).

## Steps (all from repo root; interpreter `.venv-wired/bin/python`, 3.14.6)
1. **Suite table.** Run pytest per package; record pass/fail/skip and compare against the
   2026-07-07 baseline (`reports/SHIP_VERIFY_2026-07-07.md` §1). Baseline in parentheses:
   `labs/gaslab` (208p/2s) · `labs/obdlab` (388p/2s) · `labs/dtclab` (590p) ·
   `labs/dnalab` (27p) · `labs/vinlab` (200p/8s) · `labs/comlab` (527p/4s) ·
   `labs/comlab/registry` (494p) · `apps/wired/tests` (11p) · `apps/wired/v7/tests` (48p) ·
   **NEW** `apps/ui/tests` (8p, invoke as `PYTHONPATH=apps/ui:labs/comlab pytest apps/ui/tests`).
   Counts may only GROW vs baseline; any shrink or fail is a FINDING.
2. **Guards.** (a) wired `registry_guard` expected-rule-count == rules on disk;
   (b) registry manifest==rules assertion; (c) vocabulary drift guard
   `labs/comlab/tests/unit/test_vocabulary.py`; (d) scoreboard
   (`apps/wired/fl_tasks/score_v3_yardstick.py`) → `Hash lock: ok` on
   `V3_YARDSTICK_2026-07-06-C9B`, `top3_family` **exactly 269/294**, synthetic-vs-real
   split **exactly 191 real + 78 synthetic** (C2 19 · C3 16 · C4 10 · C5 10 · C6 13 · C9 10).
   Any movement in score or split is a STOP-and-surface FINDING (owner stop ruling
   2026-07-06 — no re-tuning).
3. **UI end-to-end smoke** (headless, no browser): via `ui_payload` build the T-SHIP-UI-2
   acceptance payloads and run them through the composed engine —
   (a) the MW-002 fixture case returns MW-002 in the verdict; (b) the knife-edge/abstain
   case abstains with the expected differential (re-use the assertions already pinned in
   `apps/ui/tests/test_ui.py` + `apps/wired/tests/test_oil_cases.py`; do not write new
   engine fixtures). Additionally `python -c "import app"` (with PYTHONPATH as above)
   must import clean — proves the Streamlit page has no load-time error.
4. **Pre-push tree audit (disclose, don't act).** Record `git status --porcelain` verbatim.
   Expected dirty set = the T-SHIP-UI-3 files + ledger + note + this task's report/note +
   untracked `pyrightconfig.json`. Anything OUTSIDE that set is a FINDING. Surface a
   one-line disposition question for `pyrightconfig.json` (commit vs gitignore) — owner
   decides; do not decide here. Secrets sweep: grep the dirty files for key/token patterns
   (per T-SHIP-5 G-gate pattern list) — must be clean.
5. **Report** `SHIP_FINAL_VERIFY_2026-07-08.md`: per-suite table w/ baseline delta, guard
   results, UI smoke results, verbatim dirty-tree list + explicit-path commit list the
   owner can paste, FINDINGS list. Fill both gate blocks in the progress note.

## Success criteria
- Every suite/guard/smoke result recorded with the exact command; all green or every red a
  named FINDING (file+test), with zero source edits (`git status` delta = report + note only).
- Scoreboard identity holds: 269/294, split 191+78, hash lock ok.
- Report ends with the **owner commit list**: explicit file paths only (no `add -A`), and
  states that push/merge is the owner's action.
FORBIDDEN: editing any source/test/corpus/rule/yardstick; running `graphify`; touching
`Vault/`; git commit/branch/stash/push; re-tuning anything the score sweep flags.
