# T-V3-P4-C6A — progress note

**Task:** [[T-V3-P4-C6A_c6_signal_dryrun]] — C6 (`SensorDynamicsState`) signal-pack dry-run.  
**Date:** 2026-07-05 · **Coder:** Codex · **Mode:** STRICT (dual-gate) · **DISCLOSE half**

## What shipped (all new, under `v3/` only)

- `v3/c6_signal_sim.py` — read-only overlay simulator. Runs zero-overlay self-check first, then Scenario 1 (Mode $06 margin only), Scenario 2 (+ O2 response timing), and Scenario 3 (full contract with MAF actual-vs-calculated airflow). Pinned to `POST_T_V3_P4_C3B` / `V3_YARDSTICK_2026-07-05-C3B`.
- `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.json` — machine-readable per-scenario/per-case detail, FT-8 union, no_fault-neighbour breakout, and C3/C6 precedence assertion.
- `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.md` — essential-first 6-section reveal-contract report for owner C6B sizing.

## Findings surfaced (disclosure, not hidden)

- **Zero-overlay self-check:** drift = 0 across 294 vs `POST_T_V3_P4_C3B`.
- **Scenario 3 full contract:** `top3_family` simulates **228/294 → 241/294 (+13)** on synthetic C6 evidence.
- **Yield split (14 C6 cases):** **13 WOULD_BANK / 0 ALREADY_PASS / 1 STILL_SHORT / 0 ABSTAIN_NO_DATA**.
  - WOULD_BANK: `CASE-014, CASE-045, CASE-048, CSV-025, EXP-N020, EXT-229, EXT-230, TC-046, YAML-CSV25, YAML-TC46, case_046, era1_006, era2_012`.
  - STILL_SHORT: `PDF-4G-05` — correct; it is the stay-abstained misfire lookalike and banking it would be a back-solve alarm.
- **Covered-vs-masked at MARGIN=0.02:** of the 13 WOULD_BANK cases, **8 are covered** and **5 remain abstained**.
- **Column-subset ladder:** Scenario 1 Mode $06 = **12** WOULD_BANK; Scenario 2 +O2 timing = **12**; Scenario 3 +MAF = **13**. The six MAF/airflow columns are load-bearing only for `EXP-N020`; Mode $06 carries the 12 O2-lazy/biased rows in this seed.
- **FT-8 neighbour audit:** union re-derived live from `sensor_fault.json` + `no_fault.json` `passes_cases` = **33** cases; **9** dual target+neighbour; **0** regressions on the full 294.
- **no_fault breakout:** 13 NF-rule neighbours; 7 currently passing at baseline; **0 no_fault-neighbour regressions** and **0 healthy no_fault → fault-winner regressions**.
- **C3 precedence assertion:** no current row carries both C3 `CONTROL_REFERENCE_FAULT` and decisive C6 dynamic state. C6B still must implement the precedence point in `integration_shim.py::_score_rule` if committing.

## Commit sizing for C6B (report §6)

- Producer gates simulated: Mode $06 margin ≤ 10%; O2 response ≥ 600 ms; two-point MAF delta ≤ -15% at both idle and 2500 rpm.
- Consumer overlay simulated: boost `SF-005/SF-008/SF-001/SF-002` by +0.10 on decisive C6 dynamic evidence; prune `NF-001/NF-002` only on decisive dynamic C6 evidence; abstain state is no-op.
- Column set decision: Mode $06 recovers the 12 O2 rows; O2 timing is not incremental on this seed; MAF columns add `EXP-N020` only. C6B can choose 3-column O2 set vs 9-column full set with that explicit price.
- `PDF-4G-05` remains outside C6 commit scope; it needs a misfire discriminator, not C6 back-solving.

---

## VERIFICATION GATE — T-V3-P4-C6A

1. Compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/c6_signal_sim.py`)
2. Lint    : PASS (`/agent_workspace/.venv-wired/bin/python -m ruff check v3/c6_signal_sim.py` → OK)
3. Types   : PASS (`/agent_workspace/.venv-wired/bin/python -m pyright v3/c6_signal_sim.py` → 0 errors, 0 warnings, 0 informations)
4. Tests   : PASS (`/agent_workspace/.venv-wired/bin/python v3/c6_signal_sim.py` → drift=0, S1/S2/S3 generated; S3 13 WOULD_BANK / 1 STILL_SHORT / 0 regressions; reports written)
5. Contract: PASS (reports carry producer simulation, 3-scenario ladder, C3-precedence assertion, yield disclosure, FT-8/no_fault breakout, and C6B commit scope; 14 cases reconcile; `PDF-4G-05` outside WOULD_BANK; active scoreboard still `top3_family 228/294`, `Hash lock: ok`)
6. Orphan  : N-A (in-memory simulator only; no live field/state/code path added. Named consumer = owner C6B sizing.)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C6A

Scope         : PASS (changed files are the three task deliverables under `v3/`; no live corpus/rule/registry/engine/scorer/yardstick edit)
Composition   : PASS (read-only monkeypatch overlay restores `_score_rule`; no lab edits, no cross-lab import from a lab, no deferred path, no `Vault/`, no graphify)
Consumers     : PASS (no live mapped field added; simulator names C6B/owner as consumer and reports the future SF/NF consumers explicitly)
Literals      : PASS (Mode $06 ≤10%, O2 ≥600 ms, MAF ≤-15%, and +0.10 boost are tied to C6-PRE/C6-SYNTH and the existing C2/C3/C4 boost pattern; report preserves grounding caveats)
Docstrings    : PASS (module and helper functions document the read-only dry-run, scenario ladder, producer gates, FT-8 derivation, and report writer)
Craft (WARN)  : Depth — simulator keeps producer, overlay, summary, and report seams separate; no diagnostic logic shipped live. Deletion — no dead debug path; `scenario_results_compact` is retained because the JSON report is the machine-readable per-scenario artifact. Seam — all mapping stays in the simulator, not in wired/runtime code. Interface — task is exercised through the CLI command, matching the spec.
Result: CLEAN

## Guardrails honoured

No live corpus column · no live registry/rule edit · no live re-score/mint · no seed regeneration · MARGIN unchanged (0.02) · `run_suite.py` untouched · `Vault/` untouched · no `graphify`/frozen-graph rebuild · no secrets · new files only under `v3/`. **Unblocks `T-V3-P4-C6B`** (commit — only after owner sign-off + FT-8/no_fault risk acceptance + column-set decision).
