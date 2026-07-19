
> **Context:** GASLab PRD v2.1 (2026-06-10) · Module: GASLab · Section: Section 4 — Objective · Parent document: PRD_GASLab.md
## Section 4 — Objective

**Business benefit.** Provide chemistry ground truth that overrides ECU perception when the two diverge — eliminating the "DTC says lean, gas says rich" diagnostic dead end.

**Customer benefit.** Technicians receive a single chemical signature label (e.g. `IGNITION_MISFIRE`, `EGR_STUCK_OPEN`, `CAM_TIMING_RETARDED_MAF`) derived from first principles, not from ECU heuristics.

**Key Results:**

- **KR1:** GASLab correctly classifies ≥ 95% of synthetic boundary-grid samples in CI (`tests/fixtures/synthetic_grid.py` + `tests/generative/`).
- **KR2:** Zero cross-lab Python imports (enforced by the import-isolation audit in the validator suite).
- **KR3:** All 34 `ChemicalSignature` values are reachable (verified by `test_rule_engine_reachability.py`): 6 via DNA gate, 1 via `requires_dtc`, 3 catch-all, 2 via reasoning-grammar gate (`SAMPLE_INVALID` from the validity gate, `COOLANT_LEAK_INTERNAL` from the coolant rule), the 3 `CAM_TIMING_*` via the cam-timing rule + RPM-differential gates, and the remainder via direct bound matching.
- **KR4:** Wiki drift guard (`parse_vocabulary_thresholds`) keeps ontology numeric thresholds in sync with `GAS_VOCABULARY.md §10` in every CI run.

---


## Graph relations (explicit)

**Section 4 — Objective** DESCRIBES **GASLab PRD v2.1**
**test_rule_engine_reachability.py** VERIFIES **KR3** -- 34-signature reachability
**test_validators.py** VERIFIES **KR4** -- wiki-drift guard


