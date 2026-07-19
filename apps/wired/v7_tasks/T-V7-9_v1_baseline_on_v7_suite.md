# T-V7-9 — v1 baseline on the v7 suite (USE_V2_REGISTRY=0) + v1-vs-v2 delta
**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` (runnable now) · **Blocked by:** —
**Mode:** STRICT — runs the suite under a flag flip + writes one report; **no engine/oracle/CSV edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Why this task exists
The owner's premise is that **the v2 rebuild bought little** ("v1 ≈51%, v2 ≈48% — similar
despite a month of effort"). That premise is currently **unfalsifiable as stated**: the 51% and
48% were produced on **different rulers** (v1's per-lab suites + old v6/old-taxonomy oracle vs
the v7 multi-dim oracle), so the gap is not signal. This task produces the **first same-ruler
v1-vs-v2 number** on the v7 suite, **before any tuning**, so "did the rebuild move routing?" has
a real answer instead of two incomparable figures. No engine is changed.

## Fidelity note (read first)
The standalone full-v1 system at **`/home/m/Desktop/4dV1`** has **no end-to-end `diagnose()`** —
it is `registry/` + per-lab `TestSuite/` runners; the wired composition is a v2-era construct.
So true-v1 cannot be fed the v7 suite without building a new harness over it (a larger,
separate effort held in reserve). The **runnable** v1 proxy is the current engine's legacy path
(`USE_V2_REGISTRY=0`), whose rule logic descends from that same `4dV1/registry/`. **Step 0 below
quantifies how faithful the proxy is** — the baseline number is only as trustworthy as that
fidelity, and the report must state it explicitly (no silent "this is v1" claim).

## Signal/noise
Adds no domain field or fault. The **named consumer** is the owner's tune-or-revert decision:
the delta tells us whether v2 actually regressed, in which families, and by how much — so
tuning effort (or a v1-path revert) targets the families that genuinely got worse, not the
whole engine. One report, one decision input.

## Pinned facts (verified at authoring, 2026-06-30)
- **v1 and v2 are the same engine, one toggle.** `fault_atlas_router.py:1898` branches on
  `self._use_v2_registry`: **True** → delegate to the 68-rule v2 registry shim
  (`registry/integration_shim.py`); **False** → fall through to the native v1 routing path.
- Resolution: `lab_pipeline_aggregator.py:121` reads `USE_V2_REGISTRY` env (**default "1" = v2**).
  Router param default `use_v2_registry=True` (`fault_atlas_router.py:580`).
- The existing 48% run (`v7/runs/20260630_163900/`) was produced with the **default (v2)**.
- v7 suite entrypoint `apps/wired/v7/run_suite.py` imports `wired.composition.diagnose`; the
  registry toggle is below that boundary, so the **same corpus/oracle/scorer** apply unchanged.
- Corpus `v7/data/cases_petrol_v7.csv` (314 rows); scorer = 6-dim `score_case()`.

## Success criteria (verify against these; loop until all hold)
0. **Fidelity check (do first).** Diff the current engine's legacy-path rule set against
   `/home/m/Desktop/4dV1/registry/` (rule ids, gating, weights). Report a one-line fidelity
   verdict: *high* (proxy ≈ true v1 → baseline trustworthy), *partial* (note what diverged), or
   *low* (proxy ≠ v1 → flag that a true-v1 harness over 4dV1 is needed; do NOT overclaim). This
   verdict conditions how the headline number may be described.
1. v1 run executes the full **314** cases with `USE_V2_REGISTRY=0`. Record any cases where the
   **v1 path raises** (vs v2's clean degrade) as an explicit `v1_crash` list — do not let a v1
   exception abort the run; count and report it.
2. Produce **both** numbers on the same scorer: v1 family-routing % and v2 family-routing %
   (re-use the `20260630_163900` v2 results or re-run v2 in the same session for parity — state
   which, and confirm the v2 number reproduces 141/294 if re-run).
3. **Per-family delta table:** family · v1 ✓ · v2 ✓ · Δ · regressed/improved/same. The headline
   is the count of families where **v2 < v1** (the actual regressions) and where **v2 > v1**.
4. Confirm the flip actually changed behaviour: ≥1 case must route differently between the two
   runs (guards against a no-op toggle). If verdicts are identical across all 314, that is a
   red-flag finding — report it, do not claim a baseline.

**Authorized external source (read-only):** `/home/m/Desktop/4dV1/registry/` — for the Step-0
fidelity diff only. Read natively; copy nothing into the repo (cite findings in the report).

## Scope
**IN:**
- **Step 0 fidelity diff** vs `/home/m/Desktop/4dV1/registry/` (criterion 0).
- Run `run_suite.py` over the full corpus with `USE_V2_REGISTRY=0`; capture per-case + aggregate
  (write the v1 run under `v7/runs/<ts>_v1/`, git-excluded like the v2 runs).
- Write `apps/wired/v7_tasks/reports/V7_V1_BASELINE_<date>.md`: the **fidelity verdict** (gates
  how the number is described), the two headline numbers, the per-family delta table, the
  `v1_crash` list, the regressed-families ranking, and a one-line bottom line framed as **"on a
  common ruler, the v2 registry routes better in N families / worse in M / net ±X pts vs the v1
  legacy path"** — explicitly **not** "v2 vs the 51% figure" (different ruler).
- Log a follow-up `F-V7-V1V2` in `V7_PROGRESS.md` with the regressed-family list (input to the
  later tuning/revert decision — **not** fixed here).

**OUT:** any engine/router/registry/oracle/CSV/wiki edit; changing the toggle's default;
tuning anything; committing run JSON; `graphify`; `Vault/`. If the v1 path needs a code fix to
run at all, **stop and report** — do not patch it in this task (that becomes its own spec).

## Steps
1. Reproduce/point-to the v2 baseline number (criterion 2).
2. Run the suite with `USE_V2_REGISTRY=0`; capture results + any `v1_crash`.
3. Verify the toggle changed ≥1 verdict (criterion 4).
4. Build the per-family delta table; write `V7_V1_BASELINE_<date>.md`.
5. Log `F-V7-V1V2` in `V7_PROGRESS.md`.

## Gate (STRICT dual-gate → `progress_notes/T-V7-9.md`)
- **VERIFICATION GATE:** paste both run lines (v1 + v2), the per-family delta table, the
  toggle-changed-behaviour proof, and the `v1_crash` count.
- **CODE REVIEW:** confirm zero source edits; the toggle was set via env only; run JSON excluded.
