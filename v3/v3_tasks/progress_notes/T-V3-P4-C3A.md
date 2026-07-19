# T-V3-P4-C3A — progress note

**Task:** [[T-V3-P4-C3A_c3_signal_dryrun]] — C3 (ecu_fault / `ControlPlausibilityState`) signal-pack dry-run.
**Date:** 2026-07-05 · **Coder:** Claude Code · **Mode:** STRICT (dual-gate) · **DISCLOSE half**

## What shipped (all new, under `v3/` only)
- `v3/c3_signal_sim.py` — read-only overlay simulator. Runs the zero-overlay self-check first,
  then Scenario 1 (electrical-only) + Scenario 2 (full, incl. Δλ). Pinned to the **current**
  baseline `POST_T_V3_P4_C2B` (NOT the stale `POST_T_V3_3D` the c2/c4 sims used — C2B has landed
  since, moving the ruler 197→212; this is the C4A stale-baseline lesson applied).
- `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.json` — per-case / per-scenario detail + FT-8 union.
- `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.md` — 5-section reveal-contract report (essential-first).

## Findings surfaced (disclosure, not hidden)
- **`top3_family` 212/294 → 228/294 (+16)** under the C3 producer+consumer overlay (Scenario 2).
- **Yield split (22 C3 cases):** 16 WOULD_BANK (top-3 flip) / 0 ALREADY_PASS / 6 STILL_SHORT / 0 ABSTAIN_NO_DATA.
  - WOULD_BANK 16: `CSV-041, CSV-045, CSV-123, CSV-124, ECU-001, EXP-N002, EXP-N004, EXP-N019,
    EXT-221, TC-021, YAML-CSV41, YAML-CSV45, YAML-RULE_NOx_1, YAML-TC47, case_001, case_013`.
- **Covered vs still-abstained split (disclosed, not masked):** of the 16 top-3 flips, only **4 are
  covered**; **12 remain abstained** at MARGIN=0.02. `WOULD_BANK` tracks the top-3 flip (the pack's
  headline `top3_family` metric); whether to surface the 12 masked flips is a C3B / abstain-cal call.
- **Δλ is NOT load-bearing for yield on this seed:** Scenario 1 (electrical-only, drops the two-point
  5-gas ask) banks the **same 16** as Scenario 2. The expensive, empirical-anecdotal Δλ divergence
  term can be dropped from the C3B column set — C3B can commit the 4 electrical columns
  (`koeo_map_baro_delta_kpa`, `module_voltage_loaded_v`, `dlc_signal_ground_drop_v`,
  `bidirectional_fuel_response_ok_bool`) and defer `gas_obd_lambda_delta` / `lambda_perception_delta`.
- **Paper-separable (18) > actual top-3 flips (16):** 2 processor cases (`CSV-125`, `CSV-126`) fire the
  producer state (`CONTROL_REFERENCE_FAULT`) but ecu_fault still misses top-3 — the fixed +0.10
  consumer boost does not out-rank the rich/misfire competitors. C3B must size a stronger lift or
  accept them abstained. (Surfaced, not laundered.)
- **4 stay-abstained honoured (0 back-solve alarm):** `CASE-039, ECU-009, EXP-N005, EXP-N018` (3 POA
  physical confounder + 1 intermittent) emit producer `ABSTAIN` (seeded below every gate) and land
  outside WOULD_BANK — correct.
- **FT-8 neighbour audit:** union re-derived **live** from `ecu_fault.json` (EF-*) + `sensor_fault.json`
  (SF-*) `passes_cases` = **48** cases; **18 dual target+neighbour** (the largest dual set of any pack).
  **0 regressions** on the full 294 (Scenario 2). All 18 dual-case outcomes named explicitly in report §5.
- **Zero-overlay self-check:** drift = 0 across 294 vs `POST_T_V3_P4_C2B`, confirming baseline 212.

## Commit sizing for C3B (report §6)
Producer: lean-bias `gnd>0.20 ∧ Δλ≥0.05`, rich-bias `map_baro≥5 ∧ Δλ≥0.05`, processor
`bidir=False ∧ Vmod<12.0`. Consumer: boost EF-001/002/003, prune SF-001/002, on `CONTROL_REFERENCE_FAULT`.
Column set: 4 electrical columns sufficient (Δλ deferrable). stay-abstained 4 not committable by C3.
Two separable-but-short cases (`CSV-125`/`CSV-126`) need a stronger lift decision at C3B.

---

## VERIFICATION GATE — T-V3-P4-C3A
1. Compile : PASS  (`python -m py_compile v3/c3_signal_sim.py`)
2. Lint    : PASS  (`ruff check v3/c3_signal_sim.py` → All checks passed)
3. Types   : PASS  (`pyright v3/c3_signal_sim.py` → 0 errors, 0 warnings, 0 informations)
4. Tests   : PASS  (`python v3/c3_signal_sim.py` runs the zero-overlay self-check → OK, all 294
   matched, drift = 0 vs `POST_T_V3_P4_C2B`; then both scenarios run clean.)
5. Contract: PASS  (Report carries all 5 reveal-contract sections; 22 C3 cases reconcile
   16+0+6=22; 4 stay-abstained land outside WOULD_BANK (0 back-solve alarm); FT-8 union derived
   live = 48 with regressions listed (empty); both scenarios reported; scoreboard `score` still
   reports `top3_family 212/294` + `Hash lock: ok` — live yardstick untouched.)
6. Orphan  : N-A   (In-memory sim only; adds no live field/state/code path that can orphan. The
   producer/consumer exist solely inside the overlay; named consumer = owner C3B sizing.)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C3A
Scope         : PASS  (only the 3 deliverable files under `v3/`; every changed line traces to the
                spec's Deliverables. No live corpus/rule/registry/engine/lab edit, no mint.)
Composition   : PASS  (mirrors the c2/c4 `shim._score_rule` monkeypatch overlay pattern; restores the
                original scorer in a `finally`; no cross-lab logic added, no unauthorized import.)
Consumers     : PASS  (no live field mapped; the C3 state/consumers live only in the sim overlay and
                the named consumer is the owner + `T-V3-P4-C3B` commit sizing — signal/noise satisfied.)
Literals      : PASS  (gate constants carry grounding tags + contract cites: ground 0.20 V standardized,
                Δλ 0.05 empirical-anecdotal, MAP/BARO 5 kPa + Vmod 12.0 V manufacturer-typical; boost
                +0.10 mirrors c2/c4.)
Docstrings    : PASS  (module + every helper documented; producer gates + scenario ladder spelled out
                in the module docstring.)
Craft (WARN)  : Depth — WOULD_BANK aligned to the top-3-flip definition (the pack's `top3_family`
                metric) after the first pass surfaced a 4-vs-16 gap between a covered-only counter and
                the +16 headline; covered/abstained split now disclosed explicitly rather than hidden
                behind the abstain dial. Deletion — no debug/print residue; the intermediate
                covered-based WOULD_BANK counter was replaced, not left dead. Seam — self-check + FT-8
                derivation are separate pure helpers; per-case `still_short_reason` computed once and
                rendered, not recomputed in the report.
Result: CLEAN

## Guardrails honoured
No live corpus column · no live registry/rule edit · no live re-score · no yardstick mint · no seed
regeneration (consumed `c3_synthetic_seed_2026-07-05` as-is) · no synthesized values in live corpus ·
MARGIN unchanged (0.02) · `run_suite.py` untouched · `Vault/` untouched · no `graphify`/frozen-graph
rebuild · no secrets · new files only under `v3/`. Baseline correctly re-pinned to `POST_T_V3_P4_C2B`
(the C4A stale-baseline lesson). **Unblocks `T-V3-P4-C3B`** (commit — authored in full only after this
disclosure + owner sign-off + FT-8 clean).
