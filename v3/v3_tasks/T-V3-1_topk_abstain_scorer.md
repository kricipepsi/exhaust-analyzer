### Goal ###
Extend the v3 scoreboard so it grades the **ranked top-3 differential** and **abstention**,
not just the single winner. Add three metrics to `apps/wired/fl_tasks/score_v3_yardstick.py`:
`top3_family` (expected family in {winner} union {top-2 differential siblings}), `coverage`
(share not abstained), and `top3_on_covered`. Keep the existing single-verdict number unchanged
and still printed. Mint a new yardstick file `V3_YARDSTICK_2026-06-30.md` (because the metric
set changed) while leaving `FL_YARDSTICK_2026-06-30` untouched as the immutable BEFORE. Done
when `score_v3_yardstick.py score` prints both the frozen single-verdict block AND the new
top-3/coverage block, and a unit test pins the new metric math.

### Success criteria ###
- `apps/wired/v7/tests/` (or `apps/wired/fl_tasks/tests/`) gains
  `test_topk_scorer.py::test_top3_family_counts_runnerup` (write failing first): a case whose
  winner family is wrong but a differential sibling matches expected -> `top3_family=PASS`,
  `single_verdict=FAIL`. Passes after implementation.
- `test_topk_scorer.py::test_abstain_not_counted_wrong`: an abstained case counts against
  `coverage`, is excluded from `top3_on_covered`, and is never scored as a wrong family.
- `score_v3_yardstick.py score` on the **current** engine prints the frozen block
  (`family+state 133/294 = 45.24%`, unchanged) plus a new block with `top3_family`,
  `coverage`, `top3_on_covered`, and per-FL-mode top-3 buckets.
- `V3_YARDSTICK_2026-06-30.md` exists and pins: the metric definitions, the abstain
  floor/margin (from T-V3-0), the corpus+oracle+scorer hashes for the v3 ruler, and a one-line
  statement that `FL_YARDSTICK_2026-06-30` remains the frozen BEFORE.
- Inner loop clean (`py_compile`, `ruff`, `pyright`, `pytest -x -q` on touched tests).

### Context ###
Phase 1 of `v3/V3_PLAN.md` (section 4). The metric definitions are `V3_PLAN.md` section 3
(table) — implement them exactly. The harness already loads the corpus, scorer, and engine and
reports per-FL-mode buckets: `apps/wired/fl_tasks/score_v3_yardstick.py` (see its `score`
subcommand and the per-mode bucket print in `FL_SCOREBOARD_README_2026-06-30.md`). The
single-winner scorer it calls is `apps/wired/v7/run_suite.py::score_case` (line ~94; family read
at line ~147). **Do not modify `score_case`'s existing dimensions** — add the top-3 logic
alongside, reading the engine's `differential_siblings` list
(`labs/comlab/comlab/schemas/response.py:79-101`).

The abstain floor/margin come from T-V3-0's recommendation
(`v3/reports/V3_TOPK_CEILING_2026-06-30.md`) — read those two numbers, do not invent them.
Sibling -> family mapping: prefer the `fault_family` field on the sibling **if T-V3-3 has
shipped it**; until then, map sibling `fault_id` -> family via the same registry/KG resolve the
router uses (`fault_atlas_router.py` `_kg.resolve(fault_id).fault_family`). Reuse T-V3-0's
`measure_topk.py` mapping helper rather than writing a third copy.

Yardstick discipline (`FL_YARDSTICK_2026-06-30.md` "Yardstick rule"): a changed metric set =
a **new** yardstick file. Compute fresh SHA-256s for the v3 ruler's corpus/oracle/scorer and
record them in `V3_YARDSTICK_2026-06-30.md`. Never overwrite the frozen file or its hashes.

### Consumer (signal/noise) ###
- **Consumer:** the v3 acceptance gate (`V3_PLAN.md` section 6) and the architect's go/no-go on
  hitting 95%; the new metrics are read by humans + CI, not by the engine.
- **Code path:** `apps/wired/fl_tasks/score_v3_yardstick.py::score` (prints the new block);
  the unit test `test_topk_scorer.py` is the executable contract. No engine consumer — this is
  measurement surface only, so no live-registry/KG schema change.

### Deliverables ###
1. `apps/wired/fl_tasks/score_v3_yardstick.py` — MODIFY. Add `top3_family`, `coverage`,
   `top3_on_covered`, per-mode top-3 buckets; keep the frozen single-verdict block intact.
2. `apps/wired/.../tests/test_topk_scorer.py` — CREATE. Pins the new metric math + abstain.
3. `v3/reports/V3_YARDSTICK_2026-06-30.md` — CREATE. The v3 ruler: defs, thresholds, hashes.

### Files to touch ###
- `apps/wired/fl_tasks/score_v3_yardstick.py` (MODIFY)
- `apps/wired/.../tests/test_topk_scorer.py` (CREATE — place beside the existing run_suite tests)
- `v3/reports/V3_YARDSTICK_2026-06-30.md` (CREATE)

### Out of scope ###
No engine change (T-V3-3 adds the sibling `fault_family` field and abstain emission). No oracle
re-pin (T-V3-2). Do not alter or re-hash `FL_YARDSTICK_2026-06-30` — it is frozen. Do not change
`score_case`'s six existing dimensions. Surgical-change rule applies. GRAPH GUARDRAIL: no
`graphify`/graph rebuild. No `Vault/` edits.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py
ruff check apps/wired/fl_tasks/score_v3_yardstick.py
pyright apps/wired/fl_tasks/score_v3_yardstick.py || true   # match house pyright scope
/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired -k topk_scorer
# Frozen single-verdict number must be unchanged:
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score | grep -E '45.24|133/294'
# New block present:
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score | grep -iE 'top3|coverage'
```
All steps must pass; the frozen 45.24% must still print unchanged.

### Progress hook ###
PROGRESS.md `T-V3-1`: Status=done, Files changed=3, Verification="top3/coverage/abstain metrics added; frozen 45.24% unchanged; V3_YARDSTICK minted"
