### Goal ###
Fix `top3_family` in the scorer to count **distinct families**, as its name and definition claim.
Today both scorer sites take the first **two sibling entries** (`differential_siblings[:2]`), so when
a same-family duplicate occupies an early slot the effective window shrinks below three distinct
families and a genuine top-3 hit is undercounted. Change both sites to *winner + the first two
**distinct** non-winner sibling families* (a true 3-distinct-family window). This is a **correctness
fix to the metric**, not a widening of it — it mirrors the already-accepted family-aware precedent in
`T-V3-3C` (dedupe siblings by family). Fully implementable now: **no owner data, no corpus/oracle
change, no yardstick mint, `run_suite.py` untouched.**

### Progressive-disclosure role — implementable-in-full COMMIT with internal disclosure ###
The forward-registered note framed this as "widen the sibling window top-2 → top-3." Measurement
(read-only, already run) shows that framing is wrong twice over, and the task is authored to the
corrected shape:
1. **`EXP-N010` already banks** post-reweight/re-pin (winner_family = `rich_mixture` = expected). The
   stale note's "bank EXP-N010" is obsolete — do not treat it as a target.
2. A **naive** `[:2]→[:3]` counts winner + 3 siblings = up to **four** families and newly-passes
   **10** cases (6 of them genuinely rank-4) — a real top-3 → top-4 **loosening**. That is a separate
   acceptance-definition decision and is **out of scope** here (flag it, do not ship it).
The family-aware distinct-count fix newly-passes **4** cases and is provably regression-free, so it
ships as one complete task; its verification *is* the disclosure (report the exact delta).

### Measured delta (already computed read-only; the executor must reproduce it) ###
- Current: `top3_family = 193/294`.
- After the distinct-family fix: **197/294** — newly passing: `era1_011, era3_008, era3_015,
  YAML-CSV95` (each currently masked because a same-family duplicate crowds the first two entries).
- **No regression possible:** for every case the current set `{winner} ∪ {sib[:2]}` is a subset of
  the distinct set `{winner} ∪ {first 2 distinct non-winner families}`, so the change is monotonic
  (can only add passes). The executor must confirm `newly_fail == 0` on the per-case diff.
- **Not shipped (flagged for a separate owner call):** naive `[:3]` would add 10 (incl. 6 rank-4
  cases: it turns top3 into top4). Name them in the report; do not enable them.

### Success criteria ###
1. Both scorer sites count distinct families:
   - `score_v3_yardstick.py` main loop (~L406-417): replace the `differential_siblings[:2]` entry
     loop with one that walks siblings in rank order and collects non-winner families until **two
     distinct** are gathered (skip `unspecified`; skip any family already == `winner_family` or
     already collected). `top3_families = {winner_family} | collected`.
   - `top3_family_pass()` helper (~L614-628): apply the identical distinct-family logic so the helper
     and the main loop agree.
2. Re-score `POST_T_V3_3D`: `top3_family` reads **197/294**; `single_verdict` unchanged; per-case
   diff shows `newly_pass = {era1_011, era3_008, era3_015, YAML-CSV95}` and **`newly_fail = (empty)`**.
3. Report `top3_on_covered` honestly before/after (state whether the 4 newly-passing cases are
   covered or abstained at MARGIN=0.02, so the covered-accuracy number is not misread).
4. Hash lock stays **ok** on `V3_YARDSTICK_2026-07-01` — this touches only the non-locked scorer
   read-site, so **no re-mint**. Confirm the scoreboard still reports `Hash lock: ok`.
5. A scorer unit test asserts the distinct-family window: a synthetic verdict with siblings
   `[misfire, misfire, lean_condition]` and winner `misfire`, expected `lean_condition`, must now
   pass (it fails under the old `[:2]` logic). Keep all existing scorer tests green.
6. Inner loop: `py_compile` + `ruff` + `pyright` + `pytest` (existing suite + new test) all green.

### Disclosure (what this task must surface, not hide) ###
State plainly that `top3_family` moved 193 → 197 because the metric now counts **3 distinct
families** rather than 3 sibling *entries* — a definition correction, not new engine accuracy (no
prediction changed). Cite the `T-V3-3C` family-aware precedent. Explicitly record that the naive
top-4 widen (+10) was **declined** and list its 6 genuinely-rank-4 cases, so a future owner sees the
loosening option without it being smuggled in. Note `EXP-N010` was already banked (stale target
corrected).

### Context ###
- Scorer (NOT hash-locked; safe to edit read-sites/constants): `apps/wired/fl_tasks/score_v3_yardstick.py`
  — sites at the `top3_family` main loop and `top3_family_pass()` helper; `sibling_family()` resolver
  already exists. `ABSTAIN_MARGIN=0.02` unchanged.
- Per-case diff harness (for `newly_pass`/`newly_fail`): `score_v3_yardstick.py diff` (from `T-V3-D4`).
- Run to score: `apps/wired/v7/runs/POST_T_V3_3D/results.json`. Denominator = 294.
- Family-aware precedent: `T-V3-3C_family_aware_abstain_margin.md` (dedupe siblings to first
  different family) — same idea, applied to the abstain margin; reuse its rationale.
- Hash-lock guardrail: `run_suite.py` is the frozen scorer — **never edit it**; the yardstick hash
  covers csv/oracle/run_suite, none of which this task touches.

### Consumer (signal/noise) ###
- **Consumer:** the scoreboard `top3_family` / `top3_on_covered` metrics and the owner's acceptance
  read. No engine field/enum/rule added; no producer/consumer wiring — this is a scorer read-site
  correctness fix only.

### Deliverables ###
1. `apps/wired/fl_tasks/score_v3_yardstick.py` — EDIT (two sites → distinct-family window).
2. `apps/wired/fl_tasks/test_topk_scorer.py` (or the existing scorer test module) — EDIT/ADD the
   distinct-window test.
3. `v3/reports/V3_SCORERWIN_TOP3_DISTINCT_2026-07-01.md` — CREATE. Before/after delta, the 4
   newly-pass ids, the declined naive-widen set, covered-vs-abstained note.

### Files to touch ###
- `apps/wired/fl_tasks/score_v3_yardstick.py` (EDIT)
- `apps/wired/fl_tasks/test_topk_scorer.py` (EDIT/ADD test)
- `v3/reports/V3_SCORERWIN_TOP3_DISTINCT_2026-07-01.md` (CREATE)

### Out of scope ###
**No `run_suite.py` edit. No corpus/oracle edit. No new yardstick mint. No abstain-dial change
(MARGIN stays 0.02). No engine/lab/registry edit. No naive top-4 widen** (declined — separate owner
call). Never `Vault/`. GRAPH GUARDRAIL: no `graphify` / frozen-graph rebuild. No secrets in files.
Surgical: only the two scorer sites + one test + one report.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py
/agent_workspace/.venv-wired/bin/python -m pytest apps/wired/fl_tasks/test_topk_scorer.py -q
# metric + hash lock + monotonic no-regression:
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --results apps/wired/v7/runs/POST_T_V3_3D/results.json
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff  # newly_pass=4, newly_fail=(empty)
```
Gate: `top3_family = 197/294`; per-case diff `newly_pass = {era1_011, era3_008, era3_015,
YAML-CSV95}` and `newly_fail` empty; `single_verdict` unchanged; `Hash lock: ok` (no re-mint);
scorer suite + new distinct-window test green; `git status` shows only the two scorer files + the
report (no `run_suite.py`, no corpus/oracle).

### Progress hook ###
PROGRESS.md `T-V3-D6-SCORERWIN`: Status=done, Files changed=3, Verification="top3_family definition
corrected to count 3 DISTINCT families (winner + first 2 distinct sibling families); 193->197
(newly: era1_011/era3_008/era3_015/YAML-CSV95); monotonic, newly_fail=(empty); single_verdict
unchanged; Hash lock ok, no re-mint; naive top-4 widen (+10) declined & flagged; EXP-N010 already
banked. Cites T-V3-3C precedent."

### Depends on ###
`T-V3-3C` (family-aware precedent) + `T-V3-D4` (per-case diff harness) done. **Not owner-data-gated.**
Runnable now.
