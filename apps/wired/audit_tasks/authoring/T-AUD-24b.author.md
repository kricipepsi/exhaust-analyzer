# T-AUD-24b — authoring sidecar (Windows Cowork, 2026-11-15)

Input: T-AUD-23a verdicts CK1384/CK1389 (CO) and CK1386/CK1391 (lambda) CONTRADICTED against legal limits. Survey by
Cowork (difficulty 2: no separate survey, no cold read; code row keeps its second review). Lane: Hydrogen medium.

### Verified context ###
1. **`gas_co_max_pct` and `gas_hc_max_ppm` have no reader**: grep over labs/ and apps/ (py, yaml, json, excluding
   Vault) lists only the YAML. `HorizonContext.threshold_mask` is built but never read. Observed on 33c3d79.
2. **`lambda_tolerance` is read by lab_pipeline_aggregator._lambda_tolerance_for_horizon and used in
   fault_atlas_router._ecu_fault_verdict as |normalized_obd_lambda - lambda_chem| <= tolerance.** Read.
3. **Deleting the six lines leaves comlab 606 and wired 189.** Rehearsed and restored.
4. **wiki 04_horizon_eras.md:92-94 holds a third set of numbers (CO 1.5/1.0/0.5, HC 300/200/150).** Read.

### Rulings and the tradeoff that lost ###
- **Delete the dead keys** rather than set them to the legal limits: nothing reads them; legal values in config would
  look live. Lost: legal values with a "not read" comment.
- **Keep lambda_tolerance values**: a sensor-agreement tolerance; the legal 1 ± 0.03 window does not decide it. The
  T-AUD-23a lambda verdicts judged the label; this row fixes the label.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | P1 lines deleted then restored: `606 passed` |
| step 2 | SIMULATED | same: `189 passed` |
| step 3 | SIMULATED | pre-state `ERA FAIL [3 horizons]`; P1 lines deleted: `ERA OK` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24b: dead era CO/HC keys removed; lambda_tolerance described as OBD-vs-chemical agreement.

### Cold read ###
none (difficulty 2, process 055).

### Correction history ###
(none)
