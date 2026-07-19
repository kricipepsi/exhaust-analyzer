> **Context:** DNALab ADR_DNALab v2 (2026-06-12) · Module: DNALab · Section: ADR-0002: · Parent document: ADR_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## ADR-0002: DNALab is the only in-family importer

**Status:** Accepted (`docs/adr/0002-dnalab-only-importer.md`)

### Context

The DNA family is three isolated codebases. But composition inherently needs to call
both producers — a pure no-import rule would make composition impossible.

### Decision

Permit exactly one in-family import direction: `dnalab → vinlab + symptomlab`. VINLab and
SymptomLab import no one; DNALab imports both and imports **no** COMLab. COMLab mirrors
`VehicleDNA`.

### Consequences

- **Positive:** composition is possible without breaking lab isolation; the dependency
  graph stays acyclic and one-directional.
- **Negative:** DNALab is coupled to both producers' public APIs (intended — that is its
  job).

### Alternatives Considered

1. **No imports at all (compose via JSON only).** Rejected: would force the UI to call
   both labs and hand DNALab raw dicts, scattering the orchestration.
2. **Bidirectional imports.** Rejected: reintroduces cycles.

---

## Graph relations (explicit)

**ADR-0002** DESCRIBES **DNALab as only in-family importer** (dnalab → vinlab + symptomlab)
**dnalab** VERIFIES **one-way import direction** (VINLab/SymptomLab import no one, DNALab imports both)
**dnalab** VERIFIES **no COMLab import** (COMLab mirrors VehicleDNA)
**ADR-0002** SUPERSEDES **no-import and bidirectional alternatives** (rejected)
