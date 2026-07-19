> **Context:** VINLab PRD v2.1 (2026-06-12) | Module: VINLab | Section: Section 4 — Objective | Parent document: PRD_VINLab.md / SEMANTIC_CONTRACT section 4.1

## Section 4 — Objective

**Business benefit.** Provide a typed, confidence-graded vehicle profile at decode time
so every downstream lab can tailor its analysis to the exact hardware on the car —
without embedded per-vehicle lookup tables in each lab.

**Customer benefit.** The technician scans or types a VIN once; the app instantly knows
the engine architecture and emission targets and shows only the inputs that matter for
that specific vehicle.

**Key Results:**

- **KR1:** `decode()` runs with zero network and zero MySQL on every call (offline
  constraint; data baked into `vinlab/data/`).
- **KR2:** Out-of-scope vehicles are rejected at decode: non-petrol (H1) and model year
  outside 1990–2020 (H2) raise `VINDecodeError`.
- **KR3:** Inputs that are not 17 characters raise `ChassisNumberError` (a
  `VINDecodeError` subclass) so callers can route legacy chassis numbers separately.
- **KR4:** Every decode returns a `VinConfidence` grade (`HIGH` / `PARTIAL` / `NONE`)
  reflecting how much of the profile was resolved from authoritative data.
- **KR5:** Zero cross-lab Python imports (DNA-family boundary; COMLab mirrors `VinDNA`).
- **KR6:** Every numeric literal in `vinlab/` carries a wiki/standard citation comment.
- **KR7:** All SQL lives in `db/tecdoc_query.py` (H8 SQL-isolation); no other module
  writes SQL.

---

## Graph relations (explicit)

**Section 4 — Objective** DESCRIBES **VINLab PRD v2.1 (2026-06-12)**
**labs/vinlab/tests/unit/test_csv_suite.py** VERIFIES **vinlab.decoder.RobustVINDecoder.decode_vin_payload**
**labs/vinlab/tests/unit/test_contract_conformance.py** VERIFIES **vinlab.models.VinDNA**
