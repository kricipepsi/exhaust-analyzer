> **Context:** DNALab LLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 7. · Parent document: LLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 7. Forbidden Patterns (DNALab-specific)

| Pattern | Enforcement |
|---------|-------------|
| `from comlab/gaslab/obdlab/dtclab import …` | only in-family imports allowed (`dnalab → vinlab + symptomlab`) |
| Duplicating `VinDNA` / `SymptomDNA` field knowledge in the umbrella | delegate to each model's `to_json`/`from_json` |
| Silent cross-`schema_version` load | `from_json_payload` must raise on mismatch |
| Defining validation that belongs to a producer | DNALab pre-checks triage-key presence only |
| Numeric/physics literals in `dnalab/` | none should exist — DNALab is composition, not computation |

## Graph relations (explicit)

**dnalab** VERIFIES **only in-family imports** (dnalab → vinlab + symptomlab, no comlab/gaslab/obdlab/dtclab)
**dnalab** VERIFIES **no duplicated VinDNA/SymptomDNA field knowledge** (delegates to each model)
**from_json_payload()** VERIFIES **no silent cross-schema_version load** (raises ValueError)
**dnalab** VERIFIES **no validation that belongs to a producer** (pre-checks triage-key presence only)
**dnalab** VERIFIES **no numeric/physics literals** (composition, not computation)
