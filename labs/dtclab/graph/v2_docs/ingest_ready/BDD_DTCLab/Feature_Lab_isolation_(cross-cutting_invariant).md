
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: Lab isolation (cross-cutting invariant) · Parent document: BDD_DTCLab.md
## Feature: Lab isolation (cross-cutting invariant)
*Backing tests: `tests/unit/test_dna_view.py` (import audit).*

```gherkin
Scenario: DTCLab imports nothing from a sibling lab
  Given the dtclab package source
  When its imports are audited
  Then there is no import from gaslab, obdlab, comlab, or dnalab
  And the DNA view it consumes is its own local mirror
```


## Graph relations (explicit)

**Feature: Lab isolation (cross-cutting invariant)** DESCRIBES **DTCLab BDD v1.0**
**test_dna_view.py** VERIFIES **Feature: Lab isolation (cross-cutting invariant)**
