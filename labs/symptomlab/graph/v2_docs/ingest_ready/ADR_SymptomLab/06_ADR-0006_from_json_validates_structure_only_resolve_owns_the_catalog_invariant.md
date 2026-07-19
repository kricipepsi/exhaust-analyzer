> **Context:** SymptomLab ADR v2.1 (2026-06-12) · Module: SymptomLab · ADR-0006: `from_json` validates structure only; `resolve()` owns the catalog invariant · Parent document: ADR_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## ADR-0006: `from_json` validates structure only; `resolve()` owns the catalog invariant

**Status:** Accepted (models API)

### Context

`SymptomDNA` is both *constructed from user input* (must be catalog-checked) and
*deserialised at the JSON boundary* (already validated upstream). Running the full
catalog check on every deserialise would couple the model to the catalog file.

### Decision

`SymptomDNA.from_json()` checks **field presence + environmental enum membership** only.
The 18-pair catalog invariant is enforced by `SymptomValidator.validate()` / `resolve()`.
DNALab must build symptom records through `resolve()`; `from_json()` is for an
already-validated payload.

### Consequences

- **Positive:** deserialisation is cheap and decoupled from the catalog file.
- **Negative:** a caller that bypasses `resolve()` and hand-builds via `from_json()` can
  construct an off-catalog pair — documented in the `from_json` docstring as a
  contract callers must honour.

### Alternatives Considered

1. **Run the catalog check in `from_json` too.** Rejected: couples the model to the YAML
   and re-validates already-trusted payloads.
2. **Drop `from_json` validation entirely.** Rejected: structural/enum errors must still
   fail at the boundary.

---
---

## Graph relations (explicit)

**ADR_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**SymptomDNA.from_json** GATED_BY **structure-only validation** (enum membership + field presence)
**symptomlab.resolve** GATED_BY **catalog invariant enforcement** (pair ∈ allowed set)
