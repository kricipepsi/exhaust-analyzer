> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 16 Forbidden Patterns (OBDLab-specific) · Parent document: LLD_OBDLab.md

## 16. Forbidden Patterns (OBDLab-specific)

### Entity: Forbidden patterns and their enforcement

- **`from gaslab/dtclab/comlab/dnalab/vinlab import …`** → import-isolation audit (test suite)
- **`HIGH_IDLE_LOAD` anywhere in `obdlab/`** → `test_vocabulary.py` codebase scan
- **Numeric literal without `# wiki:` comment** → code-review gate
- **New `OBDLivePayload` field without a named consumer** → signal/noise rule — field does not ship
- **Diesel-specific logic** → `PRD_4D_App.md §5` scope exclusion

## Graph relations (explicit)

**test_dna_view.py** VERIFIES **import isolation** (0 cross-lab imports)
**test_vocabulary.py** VERIFIES **HIGH_IDLE_LOAD absent** (codebase scan)
**code-review gate** VERIFIES **every numeric literal carries # wiki: comment**
**signal/noise rule** VERIFIES **every payload field has named consumer** (no orphan fields)
**PRD_4D_App.md §5** VERIFIES **petrol-only scope** (no diesel logic)
