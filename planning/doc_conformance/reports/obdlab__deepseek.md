# Doc-Conformance Audit Report — obdlab

## Summary of Counts
- **Total Claims Checked:** 20
- **MATCH:** 16
- **DRIFT:** 3 (ChemicalSignature stale list, RpmStateBucket vs EngineStateBucket naming, OBDLivePayload vs OBDLiveDataPayload naming)
- **DUP-DRIFT:** 1 (between `labs/semantic/vocabul/OBD_VOCABULARY.md` and the other two copies)
- **SUPERSEDED:** 0
- **UNDOCUMENTED:** 0
- **PENDING:** 0

## Verdict
- **Vocabulary:** DRIFT + DUP-DRIFT (The copy of `OBD_VOCABULARY.md` at `labs/semantic/vocabul/OBD_VOCABULARY.md` contains the front matter while the other two copies in `labs/obdlab/docs/` and `labs/comlab/docs/Vocabulary/` lack it. Furthermore, §17 in all three copies is stale: it has 30 values and retains `WRONG_VALVE_TIMING`, failing to reflect the 32→34 timing split. Minor naming inconsistencies also exist: `RpmStateBucket` in code vs `EngineStateBucket` / `Engine state buckets` in docs, and `OBDLivePayload` in code vs `OBDLiveDataPayload` in docs).
- **ADR:** MATCH (All 9 ADR decisions are fully implemented in code).
- **HLD/LLD:** MATCH (All constants, sensor bounds, conversion factors, VE formulas, and O2 normaliser boundaries match the code exactly).

---

## Detailed Audit Table

| doc:line | claim | class | code evidence (file:line) | proposed fix |
|---|---|---|---|---|
| `OBD_VOCABULARY.md:status` | Preamble/front matter missing in two copies | **DUP-DRIFT** | `labs/obdlab/docs/OBD_VOCABULARY.md:1`, `labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md:1` | Overwrite the two copies with the canonical `labs/semantic/vocabul/OBD_VOCABULARY.md` content. |
| `OBD_VOCABULARY.md:573-604` | `ChemicalSignature` enum lists 30 values with `WRONG_VALVE_TIMING` | **DRIFT** | `comlab/schemas/vocabulary.py:241` (has 34 values) | Update §17 of `OBD_VOCABULARY.md` to list the 34 values and retire `WRONG_VALVE_TIMING` for `CAM_TIMING_*` states. |
| `OBD_VOCABULARY.md:83-90` | `EngineStateBucket` vs `RpmStateBucket` | **DRIFT** | `obdlab/schemas/vocabulary.py:11` | Align the naming in documentation to `RpmStateBucket` or code to `EngineStateBucket`. |
| `OBD_VOCABULARY.md:209-228` | `OBDLiveDataPayload` vs `OBDLivePayload` | **DRIFT** | `obdlab/schemas/payload.py:24` | Update documentation header and references to use `OBDLivePayload`. |
| `OBD_VOCABULARY.md:31-38` | Minimalist 8-PID schema bounds | **MATCH** | `obdlab/config/physical_sensor_bounds.json` | None |
| `OBD_VOCABULARY.md:166-170` | `VEValidity` enum values | **MATCH** | `obdlab/schemas/vocabulary.py:36` | None |
| `OBD_VOCABULARY.md:192-197` | `O2NormalizationMode` enum values | **MATCH** | `obdlab/schemas/vocabulary.py:24` | None |
| `OBD_VOCABULARY.md:200-205` | `FuelSystemStatus` enum values | **MATCH** | `obdlab/schemas/vocabulary.py:82` | None |
| `ADR_OBDLab.md:27` | ADR-0001: Revive as perception emitter, not classifier | **MATCH** | `obdlab/core/` (No classification code) | None |
| `ADR_OBDLab.md:69` | ADR-0002: Emit at Stage 2, consume at Stage 4 | **MATCH** | `labs/comlab/comlab/config/proposals/entries.yaml` | None |
| `ADR_OBDLab.md:111` | ADR-0003: No cross-lab Python imports | **MATCH** | `obdlab/` (0 cross-lab imports) | None |
| `ADR_OBDLab.md:148` | ADR-0004: Remove Physics Gate 3 | **MATCH** | `obdlab/core/semantic_consistency_checker.py` | None |
| `ADR_OBDLab.md:184` | ADR-0005: Unify exception hierarchy under `ObdLabError` | **MATCH** | `obdlab/core/exceptions.py:10` | None |
| `ADR_OBDLab.md:219` | ADR-0006: Widen trims bounds to `±127` | **MATCH** | `obdlab/config/physical_sensor_bounds.json:6` | None |
| `ADR_OBDLab.md:253` | ADR-0007: Prune dead classifier and orphan enums | **MATCH** | `obdlab/` (Checked pruned enums/classifier files) | None |
| `ADR_OBDLab.md:291` | ADR-0008: VE standard Standard formula / Single sensor gate | **MATCH** | `obdlab/core/ve_engine.py:116` | None |
| `ADR_OBDLab.md:304` | ADR-0009: Bank-2 trims are `null` on single-bank | **MATCH** | `obdlab/core/sensor_signal_translator.py` | None |
| `LLD_OBDLab.md:36-38` | `MM_AIR`, `R_GAS`, `K_OFFSET` physical constants | **MATCH** | `obdlab/core/ve_engine.py:36` | None |
| `LLD_OBDLab.md:123` | VE formula implementation details | **MATCH** | `obdlab/core/ve_engine.py:123` | None |
| `LLD_OBDLab.md:200` | O2 normalizer boundaries | **MATCH** | `obdlab/core/o2_normalizer.py:195` | None |

---

## Seeded Case Verification
- **Seeded Case Checked:** OBD vocabulary changelog and §17 staleness (does not reflect 32→34 timing split) and duplicate mirror divergence.
- **Verification Result:** **MATCH** (verified that §17 in `labs/obdlab/docs/OBD_VOCABULARY.md` contains 30 entries and is stale, and `labs/semantic/vocabul/OBD_VOCABULARY.md` has the YAML front matter while the other copies do not).
