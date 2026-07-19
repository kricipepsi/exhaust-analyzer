> **Context:** SymptomLab ADR v2.1 (2026-06-12) · Module: SymptomLab · References · Parent document: ADR_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## References

- `SEMANTIC_CONTRACT.md §4.2, §8` — `SymptomDNA` schema and environmental vocabulary.
- `VehicleDNA.md` — the triage diagram (the catalog's source).
- `DNALab_TO_COMLab_FLOW.md §4` — routing is COMLab-owned.
- `labs/dnalab/tasks/PROGRESS.md` / `docs/research/DNAresearch.md` — revised catalog +
  `load_state` (T-DNA-1, T-DNA-2) and the 65% trust ceiling.
- `HLD_SymptomLab.md` / `DLD_SymptomLab.md` / `LLD_SymptomLab.md` — current design surface.
---

## Graph relations (explicit)

**ADR_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
