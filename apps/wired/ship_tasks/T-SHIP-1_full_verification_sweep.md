# T-SHIP-1 — full-repo verification sweep (READ-ONLY disclose)
**Pack:** ship · **Status row:** `ship_tasks/SHIP_PROGRESS.md` · **Blocked by:** —
**Lane:** coder · **Write scope:** ONE report `apps/wired/ship_tasks/reports/SHIP_VERIFY_2026-07-07.md`
(+ progress note). **No source, test, corpus, rule, or yardstick file may change.**

## Why (audit B-2 + B-3 disclose half)
Last full cross-lab green was 2026-06-30 (1991 tests). Since then C2B/C3B/C5B/C4B/C6B/C9B
edited `labs/comlab/comlab/schemas/ingestion.py`, `labs/comlab/registry/integration_shim.py`,
`apps/wired/wired/composition.py`, `apps/wired/v7/load_corpus.py`, and the live corpus —
each verified only its own gates + `apps/wired/v7/tests`. Before publishing, prove the
whole tree is green, and disclose exactly how much of the headline score rests on
synthetic (provisionally seeded) data.

## Steps (all via `.sandbox-py/bin/python3.14` / `.venv-wired` per `4DLab_CLAUDE.md`)
1. **Suite table.** Run pytest per package, record pass/fail/skip counts:
   `labs/gaslab` · `labs/obdlab` · `labs/dtclab` · `labs/dnalab` · `labs/comlab` ·
   `labs/comlab/registry` · `labs/vinlab` · `apps/wired/tests` · `apps/wired/v7/tests`.
2. **Guards.** (a) wired `registry_guard` expected-rule-count matches rules on disk;
   (b) registry manifest==rules assertion; (c) `labs/comlab/tests/unit/test_vocabulary.py`
   (wiki/vocabulary drift guard); (d) scoreboard `score` → `Hash lock: ok` on
   `V3_YARDSTICK_2026-07-06-C9B`, top3_family still 269/294.
3. **Synthetic-influence map.** Join the case_ids of every `v3/data/*_synthetic_seed_*.csv`
   side file against `apps/wired/v7/runs/POST_T_V3_P4_C9B/results.json`: report, per cluster
   and in total, how many of the 269 banked (top-3 correct) cases read `synthetic=true`-seeded
   columns, and the score split banked-on-real vs banked-with-synthetic. This table is the
   input `T-SHIP-2` implements permanently.
4. **CS-002 probe** (registry follow-up `CS-002-router-assumption`): assemble one in-memory
   payload with missing chemistry + a charging DTC; assert CS-002 does NOT fire (hard-absence,
   not imputation). Record result; if it fires, that is a FINDING (fix is its own task, not here).
5. Write the report: per-suite table, guard results, synthetic split, CS-002 result,
   FINDINGS list (anything red). Fill both gate blocks in the progress note.

## Success criteria
- Every suite/guard result recorded with the exact command; zero source edits (`git status`
  delta = report + note only).
- Synthetic-influence table reconciles: banked-real + banked-synthetic = 269.
- Any failure is a named FINDING with file+test, never silently fixed in this task.
