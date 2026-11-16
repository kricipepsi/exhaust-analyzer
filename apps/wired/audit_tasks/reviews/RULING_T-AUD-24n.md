# RULING T-AUD-24n — what to fix from the T-AUD-23h mechanical_wear verdicts (Windows Cowork, 2026-11-16)

Input: `REVIEW_T-AUD-23h.md` (4 CONTRADICTED: CK0464, CK0465, CK0487, CK0502). The family never wins a v7 corpus
verdict (0 of 4 expected), so the corpus cannot measure a stricter MW gate.

## Rehearsal (CK0464, MW-003 `ect_c > 95` → `> 110`, the source's normal-band top)
`C:/4DApp/recheck/T-AUD-24n/apply.py` (rule value, description and the test pin): `labs/comlab/tests` 614 passed;
`labs/comlab/registry/tests` **1 failed**, 509 passed, 5 skipped; corpus 0 changed (family 224, code 126).
The failure is `test_oil_live_verdicts.py::test_head_gasket_routes_to_mw003`. Its head-gasket fixture
(COOLANT_LEAK_INTERNAL chemistry, coolant 98 °C) routes to CF-001 once the ECT weight is gone. The tree is restored.

## Rulings
1. **No fix: CK0464.** The gate fires inside the healthy band, but it is the weight that lets MW-003 win on its own
   chemistry (COOLANT_LEAK_INTERNAL). Without it, a head-gasket signature becomes a catalyst verdict. Moving the
   value trades a weak gate for a wrong answer. The real defect is that CF-001 outscores MW-003 on coolant-leak
   chemistry, which is a scoring design question; it is recorded here, not opened as a row (no corpus case shows it).
   Lost: the fix at 110 with the fixture moved to 112 °C (the test would then pin a value the corpus never tests).
2. **No fix: CK0465** (v1 description value), **CK0487** (NOx < 80: the same weak discriminator as T-AUD-24m) and
   **CK0502** (REVIEW_T-AUD-23h M1: a "not rich" discriminator by design).
