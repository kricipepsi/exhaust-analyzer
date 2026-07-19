# labs/symptomlab — SymptomLab v2

**Role:** operator-symptom predictiveness. Part of the DNA family but migrated as an
**independent module** (own folder, own `pyproject.toml`). Outputs feed the **COMLab prior**.
The symptom prior must stay a **prior**, never an override.
**Code origin:** fork of v1 `DNALab/SymptomLab/`; v1 archived once built and green (Phase 5).
**Boundary:** no cross-lab Python imports — COMLab mirrors the prior's types locally.

_Status: migrated 2026-06-06 (T-RM-2-DNA, sibling split). v1 process history left in `DNALab/SymptomLab/` for Phase-5 archive._
