# Doc-Conformance Audit Report — gaslab

## Summary of Counts
- **Total Claims Checked:** 30
- **MATCH:** 29
- **DRIFT:** 0
- **DUP-DRIFT:** 1 (between `labs/gaslab/docs/GAS_VOCABULARY.md` and `labs/semantic/vocabul/GAS_VOCABULARY.md`)
- **SUPERSEDED:** 0
- **UNDOCUMENTED:** 0
- **PENDING:** 0

## Verdict
- **Vocabulary:** DUP-DRIFT (The gaslab canonical vocabulary is at v2.2 and matches the code perfectly. However, the duplicate mirror in `labs/semantic/vocabul/GAS_VOCABULARY.md` is stale at v2.0, missing several updates including derived metrics, `lambda_measured`, and chunked wiki references).
- **ADR:** MATCH (All 11 ADR decisions are fully implemented in code and reflect current behavior).
- **HLD/LLD:** MATCH (All physical constants, formulas, validity thresholds, definitive overrides, and RPM-differential gates match the code exactly).

---

## Detailed Audit Table

| doc:line | claim | class | code evidence (file:line) | proposed fix |
|---|---|---|---|---|
| `GAS_VOCABULARY.md:6-16` | Front-matter implements and drift_guards mapping | **MATCH** | `gaslab/contracts.py:1`, `gaslab/tests/unit/test_contracts.py:1` | None |
| `GAS_VOCABULARY.md:75-80` | `GasReading` dataclass structure | **MATCH** | `gaslab/contracts.py:130` | None |
| `GAS_VOCABULARY.md:95-135` | `ChemicalSignature` enum (34-value contract surface; retired `WRONG_VALVE_TIMING`) | **MATCH** | `gaslab/contracts.py:32` | None |
| `GAS_VOCABULARY.md:185-193` | `LambdaBand` enum values | **MATCH** | `gaslab/contracts.py:75` | None |
| `GAS_VOCABULARY.md:199-207` | `LambdaBand` discretiser thresholds | **MATCH** | `gaslab/contracts.py:75` / `gaslab/tests/unit/test_contracts.py:55` | None |
| `GAS_VOCABULARY.md:216-221` | `SampleValidity` enum values | **MATCH** | `gaslab/contracts.py:87` | None |
| `GAS_VOCABULARY.md:239` | `Hcv` physical constant is 1.85 | **MATCH** | `gaslab/contracts.py:22` | None |
| `GAS_VOCABULARY.md:240` | `AFR_stoich` physical constant is 14.71 | **MATCH** | `gaslab/contracts.py:23` | None |
| `GAS_VOCABULARY.md:279-284` | `EngineStateBucket` enum values | **MATCH** | `gaslab/contracts.py:96` | None |
| `GAS_VOCABULARY.md:302-309` | `GasBehavior` enum values | **MATCH** | `gaslab/contracts.py:105` | None |
| `GAS_VOCABULARY.md:320-325` | `CatalystStatus` enum values | **MATCH** | `gaslab/contracts.py:116` | None |
| `GAS_VOCABULARY.md:480-489` | `GasLabPayload` Pydantic schema model with `lambda_measured` | **MATCH** | `gaslab/contracts.py:165` | None |
| `GAS_VOCABULARY.md:status` | Duplicate mirror at `labs/semantic/vocabul/GAS_VOCABULARY.md` is stale | **DUP-DRIFT** | `labs/semantic/vocabul/GAS_VOCABULARY.md:1` | Overwrite `labs/semantic/vocabul/GAS_VOCABULARY.md` with the content of `labs/gaslab/docs/GAS_VOCABULARY.md` during the reconciliation phase. |
| `ADR_GASLab.md:26` | ADR-0001: Brettschneider chemistry is ground truth over ECU perception | **MATCH** | `gaslab/brettschneider.py:11`, `gaslab/process.py` | None |
| `ADR_GASLab.md:48` | ADR-0002: Signal/noise — every schema field needs a named consumer | **MATCH** | `gaslab/contracts.py:165` (Pydantic model fields verified) | None |
| `ADR_GASLab.md:70` | ADR-0003: No cross-lab Python imports | **MATCH** | `gaslab/` (Checked 0 cross-lab imports) | None |
| `ADR_GASLab.md:92` | ADR-0004: Declarative YAML ontology as single source of fault signatures | **MATCH** | `gaslab/data/gas_lab_ontology.yaml:1`, `gaslab/ontology_loader.py` | None |
| `ADR_GASLab.md:114` | ADR-0005: DNA gates are strict and unconditional | **MATCH** | `gaslab/resolution.py:101-102` | None |
| `ADR_GASLab.md:136` | ADR-0006: Deterministic specificity ranking with catch-alls last | **MATCH** | `gaslab/rule_engine.py:36` | None |
| `ADR_GASLab.md:158` | ADR-0007: Retire `WRONG_VALVE_TIMING`; adopt three `CAM_TIMING_*` states | **MATCH** | `gaslab/contracts.py:32` | None |
| `ADR_GASLab.md:180` | ADR-0008: Cam-timing states are not DNA-gated | **MATCH** | `gaslab/resolution.py:101-102` (No DNA gate filters applied to them) | None |
| `ADR_GASLab.md:202` | ADR-0009: Optional high-idle reading drives RPM-differential separation | **MATCH** | `gaslab/process.py`, `gaslab/resolution.py:201` | None |
| `ADR_GASLab.md:224` | ADR-0010: Collapse `target_lambda` pair into a single `target_lambda_v112` window | **MATCH** | `gaslab/rule_engine.py:134` | None |
| `ADR_GASLab.md:246` | ADR-0011: `confidence` gates only the `co_high_idle` override | **MATCH** | `gaslab/resolution.py:255` | None |
| `LLD_GASLab.md:24` | `HC_FACTOR` is 0.0025 | **MATCH** | `gaslab/contracts.py:24` | None |
| `LLD_GASLab.md:69` | `lambda_chem` implementation details | **MATCH** | `gaslab/brettschneider.py:11` | None |
| `LLD_GASLab.md:97-104` | Triangle and dilution gates thresholds | **MATCH** | `gaslab/validity_gates.py:25`, `gaslab/validity_gates:47` | None |
| `LLD_GASLab.md:123` | Definitive overrides (`_definitive_match` in firing order) | **MATCH** | `gaslab/rule_engine.py:243` | None |
| `LLD_GASLab.md:201` | RPM-differential family separation gates | **MATCH** | `gaslab/resolution.py:apply_differentiators` | None |
| `LLD_GASLab.md:275` | Euro-Class scaling thresholds table | **MATCH** | `gaslab/resolution.py:282` | None |

---

## Seeded Case Verification
- **Seeded Case Checked:** `ChemicalSignature` has exactly 34 enum members, `WRONG_VALVE_TIMING` is retired, and three `CAM_TIMING_*` members are present.
- **Verification Result:** **MATCH** (verified in `labs/gaslab/gaslab/contracts.py:32` and `labs/gaslab/tests/unit/test_contracts.py:26` - all tests pass).
