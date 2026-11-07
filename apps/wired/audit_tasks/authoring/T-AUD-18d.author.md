# T-AUD-18d — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_comlab.md` SEMANTIC_CONTRACT section (group 6 of `reviews/REVIEW_T-AUD-11g.md`)
and the T-AUD-18 ledger note on the vocabulary copies.
Rehearsal: `C:/4DApp/recheck/T-AUD-18d/` (`apply_fix.py`, `census.sh`, `rehearsal.patch`, `enums.py`, `chem.py`).

### Verified context ###
1. **COMLab code on `fix/T-AUD-18b`:** `DTCRoutingTag` 17 values, equal to DTCLab's; `Mode06Status` 4 values with
   `Mode06MonitorState = Mode06Status`; `ChemicalSignature` 34 values, no `WRONG_VALVE_TIMING`; `DTCFallbackStrategy`
   3 values (COMLab only). `enums.py`, `chem.py`. Observed.
2. **Fields:** `secondary_air_equipped` in no non-test `.py` under `labs/`; `reading_high` only in
   `labs/gaslab/gaslab/process.py`; `mode_06_monitors: dict[str, Mode06MonitorResult]` (`monitor_id`, `state`,
   `margin_pct`, `target_component`); `ff_fuel_spark_cut_at_crank` read by `fault_atlas_router.py`. grep. Observed.
3. **metadata:** `metadata: SessionMetadata` required, `vehicle_dna: VehicleDNA | None = None`, validator
   `_metadata_from_vehicle_dna` derives one from the other (`schemas/ingestion.py`). The drift finding is half stale;
   the doc still says COMLab reads `vehicle_dna.*`. Observed.
4. **run_fallback_tree:** returns on `suppress_gaslab`, else raises `NotImplementedError` (phase 3). Observed.
5. **Copies vs originals:** DTC 59 diff lines (with front matter), OBD 21. Every disputed fact matches the original and
   the COMLab code (fact 1, 2). Observed.
6. **Rehearsal** (restored): census `42/21/0/5` → `13/4/6/0`; 3 files; comlab `503 passed, 4 skipped, 2 errors` equal
   (`test_vocabulary.py`, `test_t_aud_4q_no_projector.py` read the copies). Observed.

### Rulings and the tradeoff that lost ###
- **R1 copies follow originals, COMLab-only parts kept.** Lost: a pointer file in place of each copy (the COMLab drift
  guard reads the copies, and the HLD names them); lost: copying the front matter (it names the original as `source`).
- **R2 SEMANTIC_CONTRACT follows code.** The `run_fallback_tree` line (group 2) is taken here because it is in this
  file and the fact is not in dispute; the HLD side and any ruling to build the tree stay in T-AUD-18e. Lost: leaving
  the line to 18e (two rows editing one file).
- Docs row: no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `dtc_diff 13`; `obd_diff 4`; `sc_marks 6`; `sc_stale 0`; three files |
| step 2 | SIMULATED | `503 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-18d: COMLab DTC/OBD vocabulary copies resynced to the lab originals; SEMANTIC_CONTRACT follows the code (6 marks).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (fact 6) · `apply_fix.py` exits on any literal count other than 1 · traceability:
criteria 1-3 → steps 1-3 · 1c grep: "exactly" in P2 is the measured three-file list · cold read: not triggered (d1,
scripted, the 18a-18c pattern) · no finding.

### Correction history ###
(none)
