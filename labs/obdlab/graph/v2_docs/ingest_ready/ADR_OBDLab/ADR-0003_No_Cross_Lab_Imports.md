> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0003: No cross-lab Python imports · Parent document: ADR_OBDLab.md

## ADR-0003: No cross-lab Python imports — OBDLab mirrors the types it needs

**Status:** Accepted (architecture constraint; exercised by T-OBDV2-6)

### Context

The 4D architecture keeps each lab a fully isolated codebase connected only
through typed JSON boundaries. OBDLab nonetheless needs types that originate
elsewhere — e.g. fuel-system loop status, which DTCLab defines
(`DTC_VOCABULARY §8`).

### Decision

OBDLab **never imports** from `gaslab`, `dtclab`, `comlab`, `dnalab`, or
`vinlab`. When it needs a cross-lab type it **mirrors a local copy** — e.g.
`FuelSystemStatus` in `schemas/vocabulary.py`, sourced verbatim from
`DTC_VOCABULARY §8`, with a `from_wire()` coercion for legacy strings. The DNA
view is likewise an OBDLab-owned mirror (`ObdLabDnaView`) of the COMLab DNA
projection. An import-isolation audit in the test suite enforces this.

### Consequences

- **Positive:** labs build, test, and version independently; no import cycles.
- **Positive:** the wire contract is explicit and drift-guarded by tests.
- **Negative:** mirrored types can drift from their source of truth; sync is a
  manual, documented responsibility (e.g. COMLab keeps the DTC frozensets in
  sync).

### Alternatives Considered

1. **Shared `common` package** of cross-lab enums. Rejected: reintroduces the
   coupling the isolation rule exists to remove.
2. **Direct import from DTCLab** for `FuelSystemStatus`. Rejected: violates the
   no-cross-lab-import constraint.

## Graph relations (explicit)

**ADR-0003** DESCRIBES **No cross-lab Python imports** (lab isolation via typed JSON boundaries)
**T-OBDV2-6** DESCRIBES **ADR-0003** (FuelSystemStatus mirror exercise)
**FuelSystemStatus** MIRRORS_CONTRACT_IN **DTC_VOCABULARY §8** (local copy with from_wire() coercion)
**ObdLabDnaView** MIRRORS_CONTRACT_IN **COMLab DNA projection** (OBDLab-owned mirror)
**test_dna_view.py** VERIFIES **import isolation** (0 cross-lab imports)
