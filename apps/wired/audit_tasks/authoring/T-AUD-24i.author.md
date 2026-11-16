# T-AUD-24i — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-23c ruling §5 (CK0592, CK0012, CK0440; `reviews/RULING_T-AUD-23c.md`). Survey and corpus by Cowork
(difficulty 2: no cold read; second review kept, code row). Lane: Hydrogen medium.

### Verified context ###
1. **Corpus (v7, 314): R1-R3 applied → 0 verdicts change (221 of 314).** Measured on 373e72c (recheck/T-AUD-24i/).
2. **Suites with R1-R4: comlab 610, registry 510/5 — equal to base.** Without R4 the registry suite fails 1
   (`test_ov001_ect_definitive_110`). Rehearsed and restored.
3. **OBD_VOCABULARY §23.1 `OVERHEATING_THRESHOLD` `≥ 108°C`** (`labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md:754`);
   GASLab LEAN_MIXTURE `lambda: { min: 1.05 }` (`gas_lab_ontology.yaml:126`); delta-relations/07 GAS-FC-001 O2 2.50
   at 2500 rpm (`Vault/labs/obdlab/wiki/delta-relations/07_gas-transition-matrix-2speed.md:38`). Read.
4. **Step 3 on base prints `24i FAIL (('gt', 110.0), '2.0', False)`; patched `24i OK`.** Run.

### Rulings and the tradeoff that lost ###
- **`ge 108`, not `gt 108`**: the vocabulary says `≥`. Lost: keep `gt`; it differs only at exactly 108.0 but
  leaves the drift in place.
- **Code to the vocabulary, not the vocabulary to the code**: the OV-001 description already names
  OVERHEATING_THRESHOLD. Lost: edit OBD_VOCABULARY to 110 (a doc change to suit a value with no source).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | patch applied: `610 passed` |
| step 2 | SIMULATED | patch applied: `510 passed, 5 skipped` |
| step 3 | SIMULATED | pre `24i FAIL`; patched `24i OK (('ge', 108.0), '2.5', True)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24i: OV-001 ge 108, flat-cam O2 2.5, LC-001 text 1.05; corpus 0 changed.

### Cold read ###
none (difficulty 2, process 055).

### Correction history ###
(none)
