# P6 Ship Gate Report — T-P6-3

**Date:** 2026-05-10
**Tool:** `dev/run_corpus.py`, pytest suites, mutmut
**Corpus:** `cases/csv/cases_petrol_master_v6.csv` (400 cases)

---

## Gate Summary

| Gate | Name | Result | Score | Threshold | Detail |
|------|------|--------|-------|-----------|--------|
| 1 | pytest Layer-1 | **PASS** | 587/587 | 100% green | Full suite green in 2.16s |
| 2 | Layer-2 corpus replay | **FAIL** | 4.8% family | ≥75% family | 19/400 family match. Documented structural floor (T-P6-2 calibration log). |
| 3 | KR3 Truth-vs-Perception | **PASS** | 28/28 (100%) | 100% | Layer-4 gate met |
| 4 | Perturbation suite | **FAIL** | 0 tests | ≥95% same-family | `tests/v2/perturbation/` directory exists but is empty — no tests built |
| 5 | Schema invariants | **PASS** | 5/5 | 0 failures | Discriminators, era, magnet edges, provenance, aliases |
| 6 | Petrol-only lint | **PASS** | 2/2 | 0 violations | engine/v2/ and schema/v2/ clean |
| 7 | Threshold provenance | **PASS** | 199 sourced | 0 unsourced | Every threshold in `thresholds.yaml` has `# source_guide:` |
| 8 | Mutation score | **SKIP** | — | ≥80% | Platform limitation: mutmut requires WSL on Windows (github.com/boxed/mutmut/issues/397) |

**Overall verdict: BLOCKED** — Gates 2 and 4 failed. Gate 8 skipped (platform limitation).

---

## Gate 1 — pytest Layer-1

```
============================= 587 passed in 2.16s =============================
```

All 587 tests across unit, integration, schema invariants, KR3, properties,
petrol lint, and corpus replay pass green. No regressions.

## Gate 2 — Layer-2 Corpus Replay

```
Corpus: cases/csv/cases_petrol_master_v6.csv
Cases:  400
Processed: 400/400 cases in 0.4s
State accuracy:  44/400 = 11.0%
Family accuracy: 19/400 = 4.8%
```

**Required:** ≥75% top-1 family accuracy, ≥50% specific-node accuracy.
**Actual:** 4.8% family, 11.0% state.

This is the documented pre-structural-fix floor from T-P6-2 calibration
(see `results/P6_calibration_log.md`). The dominant failure mode is
`Fuel_Delivery_Low` returning as V2 top-1 on ~62% of cases due to its
7 incoming positive edges combining to a near-ceiling CF whenever
lean-related symptoms fire.

**Root cause (from T-P6-2 calibration log):**
- M2 `gas_lab.py`: `SYM_LAMBDA_HIGH` triggers at λ > 1.03 and
  `SYM_IDLE_STOICH_LOAD_LEAN` triggers on any positive STFT at idle —
  both fire on almost every lean-ish case.
- M4 `kg_engine.py`: `Fuel_Delivery_Low` has only one inhibitory edge
  (`SYM_DTC_INDUCTION` at −0.17); no inhibitory edges from
  fuel-contradictory symptoms.
- M3 `arbitrator.py`: Flood control (R8) does not limit
  `Fuel_Delivery_Low` when > 3 sibling symptoms fire.
- M2 `gas_lab.py`: `SYM_LATE_TIMING_PATTERN` is never emitted despite
  having a 0.50 edge to `Cam_Timing_Retard_Late`.

**Required structural fixes (unplanned follow-ups T-P6-2b through T-P6-2e)
are listed in `V2_PROGRESS.md`. The calibration-only ceiling has been
reached; further accuracy improvements require edge-weight rebalancing
and symptom-detection threshold tightening.**

## Gate 3 — KR3 Truth-vs-Perception (Layer-4)

```
============================= 28 passed in 0.34s ==============================
```

All 28 KR3 tests pass: perception gap detection (lean-seen-rich,
rich-seen-lean, delta below threshold, same side no gap), gas-truth
over ECU-perception (rich truth → rich faults higher, lean truth →
lean faults higher, ECU-only follows digital), gap-must-fire
parametrize (10 cases), gap-must-not-fire (5 cases), pass rate gate,
perception gap never zeros fault scores, gas symptoms present when gap
fires, confidence ceiling respected, perception not authority (L01).

**KR3 pass rate:** 100% (≥ P4 gate of 80%, ≥ P6 gate of 100%).

## Gate 4 — Perturbation Suite (Layer-3)

```
============================ no tests ran in 0.16s =============================
```

`tests/v2/perturbation/` directory was created on 2026-05-08 but contains
no test files (only `.` and `..`). No perturbation test suite was built
during P6. The CI guard catalogue lists perturbation tests as "Phase built:
P6" but no P6 task created them.

**This is a missing deliverable, not a regression.** Perturbation tests need
to be written before the ship gate can clear.

## Gate 5 — Schema Invariants

```
tests/v2/schema_invariants/test_aliases_resolve.py PASSED
tests/v2/schema_invariants/test_era_validity.py PASSED
tests/v2/schema_invariants/test_no_magnet_edges.py PASSED
tests/v2/schema_invariants/test_threshold_provenance.py PASSED
tests/v2/schema_invariants/test_unique_discriminators.py PASSED
============================== 5 passed in 0.40s ==============================
```

All 5 schema invariant tests green. Enforces: R5/L03 (unique discriminators
among siblings), R6 (era validity), R7/L07 (no magnet edges > 0.30 without
discriminator gate), R10/L08 (threshold provenance), L09 (alias resolution).

## Gate 6 — Petrol-Only Lint

```
tests/v2/unit/test_petrol_only_lint.py::test_engine_v2_no_forbidden_tokens PASSED
tests/v2/unit/test_petrol_only_lint.py::test_schema_v2_no_forbidden_tokens PASSED
============================== 2 passed in 0.17s ==============================
```

Zero occurrences of `lpg`, `cng`, `e85`, `diesel`, or `hybrid` in
`engine/v2/` or `schema/v2/`. R12/L20 enforced.

## Gate 7 — Threshold Provenance

```
199 source_guide references found in schema/v2/thresholds.yaml
0 unsourced thresholds
```

Every numeric threshold in `schema/v2/thresholds.yaml` carries a
`# source_guide:` comment citing a master guide section. R10/L08
satisfied. The P0 master guide suite (EGR, ECU, freeze frame,
perception, NOx, turbo, exhaust) provides provenance for all 197
thresholds from the T-P0-4 audit.

## Gate 8 — Mutation Score

```
mutmut requires WSL on Windows. Native Windows support is tracked in
github.com/boxed/mutmut/issues/397
```

**Result: SKIP.** Cannot run `mutmut run` on this Windows host. The
mutation-score gate (≥80%) can only be verified on Linux/macOS or via
WSL. This is not a code defect — the tool simply does not support the
platform.

**If this gate must pass for ship:** run on a WSL instance or Linux CI
runner with:
```bash
mutmut run --paths-to-mutate "engine/v2/ranker.py,engine/v2/arbitrator.py,engine/v2/kg_engine.py,engine/v2/validation.py"
mutmut results
```

---

## V1 Plateau Structural Guards — Status

| Guard | Pattern | Status |
|-------|---------|--------|
| L01 | No perception global override | KR3 enforced (Gate 3) |
| L02 | Single resolve_conflicts() in M5 | test_resolve_conflicts_order.py green (Gate 1) |
| L03 | No sibling duplicate discriminators | test_unique_discriminators.py green (Gate 5) |
| L04 | VL mandatory and first | test_validation_layer.py green (Gate 1) |
| L05 | raw_score vs confidence separation | test_result_schema.py green (Gate 1) |
| L06 | Unified result schema across pathways | test_result_schema.py green (Gate 1) |
| L07 | No magnet edges | test_no_magnet_edges.py green (Gate 5) |
| L08 | Threshold provenance | 199 sourced, 0 unsourced (Gate 7) |
| L09 | Aliases for removed nodes | test_aliases_resolve.py green (Gate 5) |
| L10 | vref.db populated | 68 rows, 20 brands (T-P1-7) |
| L11 | Master guides written before module merges | 7 guides complete (P0) |
| L12 | No edge-weight tuning to chase accuracy | Structural fixes prioritized (T-P6-2 log) |
| L13 | Corpus replay in CI from day one | run_corpus.py running (Gate 2) |
| L14 | Perturbation suite | **MISSING** — no tests built (Gate 4) |
| L15 | Engine-state FSM as M0 primary output | test_dna_core.py green (Gate 1) |
| L16 | Confidence ceiling keyed on evidence layers | test_result_schema.py green (Gate 1) |
| L17 | UI derived from DiagnosticInput | input_model.py dataclass used by app.py |
| L18 | Fuel-status gate before trim-derived symptoms | M1 fuel-status sub-module in digital_parser.py |
| L19 | No "healthy engine" pseudo-fault | insufficient_evidence state used |
| L20 | Petrol-only as CI lint | test_petrol_only_lint.py green (Gate 6) |

**19 of 20 guards active. L14 (perturbation suite) is the single missing guard.**

---

## Conclusion

V2 is **not shippable** in its current state. The two blocking failures are:

1. **Layer-2 corpus accuracy at 4.8% (target ≥75%).** This is the
   documented structural floor, not a surprise. The calibration log from
   T-P6-2 documents the root cause (`Fuel_Delivery_Low` dominance) and
   lists 4 structural follow-ups (T-P6-2b through T-P6-2e) targeting
   `gas_lab.py`, `kg_engine.py`, and `arbitrator.py`. These are the
   minimum needed to break the 44% V1 plateau.

2. **Missing perturbation suite (Layer-3).** `tests/v2/perturbation/` is
   an empty directory. No P6 task created perturbation tests. This is a
   scoping gap — the P6 task list (T-P6-1 through T-P6-4) does not
   include a perturbation-test-building task.

The remaining 5 gates (pytest, KR3, schema invariants, petrol lint,
provenance) are healthy. Mutation testing (gate 8) requires WSL/linux
and was skipped. The V1 failure guard infrastructure (L01–L20) has 19
of 20 guards active — L14 (perturbation suite) is the sole missing guard.
