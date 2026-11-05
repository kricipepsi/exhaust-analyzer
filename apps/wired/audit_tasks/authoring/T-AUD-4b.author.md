# T-AUD-4b — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **F-C4-3 holds in code order** at the 4a tip: `diagnose` runs `_run_gaslab` and `_run_obdlab` on the decoded
   `vin_dna`, then writes the overrides into a local `emissions` copy that only the request's `has_catalyst` and
   `downstream_trim_role` read. Observed (read).
2. **The audit's f3 case no longer shows it**: `era2_015`/`era2_003` decoding changed with the T-VINA rows; the probe
   `-k f3` prints the same verdict both ways. Observed.
3. **Corpus** (`rehearse.py`): 1 of 314 cases decodes wideband; under a NARROWBAND override the base ignores it
   (LC-002, OBDLab WIDEBAND_LINEAR) and the fix gives `OBD_INPUT_INCOMPLETE` with OBDLab NARROWBAND_0_TO_1V (the case
   has only a wideband reading). 0 exceptions either way. Observed.
4. **F-C4-7**: `_build_obd_dna_view` raises on SUPERCHARGED (probe `-k f6`, and the rehearsal). OBDLab's only
   `InductionType` reader is `ve_engine.py` (`induction_raw == InductionType.NATURALLY_ASPIRATED.value`). Observed.
5. GASLab's DNA view reads `upstream_o2_type` and `has_catalyst` from `emissions` (`_build_gas_dna_view`). Observed.

### Rulings and the tradeoff that lost ###
- Overrides applied before every lab and before the required-key check. Lost: keep the required key from the decoded
  type (a narrowband reading under a narrowband override would still be refused — the f3b crash).
- SUPERCHARGED → TURBOCHARGED at the composition boundary. Lost: add SUPERCHARGED to OBDLab's enum (a lab vocabulary
  change with one reader that only asks "NA or not").
- O₂ NONE out of scope: no producer emits it; mapping it would invent a sensor. Lost: closing F-C4-7 in full.
- T-AUD-1d folds in as `test_upstream_o2_override_reaches_obdlab_and_gaslab`.
- Difficulty 3, plan NONE; code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base wired `41 passed` (2026-11-05, 4a tip) |
| step 2 | RAN | ui `30 passed`, dnalab `27 passed`, obdlab `388 passed, 2 skipped`, gaslab `208 passed, 2 skipped, 4 deselected` |
| step 3 | RAN | comlab `526 passed, 4 skipped, 2 errors` |
| step 4 | SIMULATED | `rehearse.py` applies the override through the `_build_metadata` hook: P2 |
| step 5 | DEFERRED | ruff and the log are the observables |

### Exclusivity ###
No other implementer runs. T-AUD-4c-e follow; T-AUD-4c also edits `composition.py` (after this row).

### Progress hook ###
T-AUD-4b: overrides reach GASLab/OBDLab before the labs run; SUPERCHARGED projects as TURBOCHARGED; T-AUD-1d folded.

### Cold read ###
own pass 2026-11-05: P1-P3 measured · literals found once (`overrides = _as_dict(raw_inputs.get("overrides"))`,
`induction_type=OBDInductionType(vin_dna.get("induction_type", "NATURALLY_ASPIRATED"))`) · counts: 41 + 5 = 46 ·
traceability: criteria 1-4 → steps 1-5. cold read: skipped (difficulty 3; the second review covers the code).

### Correction history ###
(none)
