> **Context:** DNALab BDD_DNALab v2 (2026-06-12) · Module: DNALab · Section: Feature: · Parent document: BDD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Feature: Isolation (CI-level behaviour)

```gherkin
Feature: DNALab imports only its two in-family producers

  Scenario: Only in-family imports exist
    Given the dnalab package
    When the import audit runs
    Then it imports vinlab and symptomlab and imports no comlab, gaslab, obdlab, or dtclab
```
*Maps to:* import-direction audit (`docs/adr/0002-dnalab-only-importer.md`).

---

## Graph relations (explicit)

**dnalab** VERIFIES **imports only vinlab + symptomlab** (no comlab, gaslab, obdlab, dtclab)
**dnalab** VERIFIES **import-direction audit** (docs/adr/0002-dnalab-only-importer.md)
