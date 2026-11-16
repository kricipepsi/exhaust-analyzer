# T-GASA-19 — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-GASA-FEURO (deferred row, found by the T-AUD-22a review), unblocked by T-GASA-17 (Euro table verified at
S009) and scoped by T-AUD-23c (GK0049-56, GK0078/79, GK0183/84, GK0091/94). Difficulty 3: survey by Cowork; plan not
needed (exact text); second review kept (code row). Lane: Hydrogen high.

### Verified context ###
1. **S009 Table 1 (DVSA, primary, fetched by T-GASA-17):** 1/8/75-1/8/86 CO 4.5 %, HC 1200; 1/8/86-1/8/95 (not Annex)
   3.5 %, HC 1200; 1/8/95-31/8/02 idle CO 0.5 %, fast idle CO 0.3 %, HC 200, λ 1±0.03; from 1/9/02 idle CO 0.3 %,
   fast idle CO 0.2 %, HC 200. Read at `labs/gaslab/audit_tasks/wikiaudit/sources/S009.md:430-438`.
2. **wiki/06b:42 (W0703, W0704): CAM_TIMING_RETARDED_MAP at 2500 rpm HC 200-600 ppm, CO 1.5-4.5 %.** claims.csv.
3. **`test_resolution.py:499-527` names the floor "the literal 1.5 (mild_rich.max)"** with a HIGH per-vehicle override:
   the Euro idle limit replaced that literal later. Read.
4. **Corpus (v7, 314): R1-R4 → 0 changed; CO ceiling 0 for Euro 3-4 → 0 changed (paths not reached).** Measured on
   c06b137 (recheck/T-GASA-FEURO/).
5. **Rehearsal (recheck/T-GASA-FEURO/rehearsal.diff): gaslab 279 → 280 (+1 new test), comlab 610, registry 510/5;
   ruff clean; on base code (a), (c), (d) fail.** Applied and reverted.

### Rulings and the tradeoff that lost ###
- **Euro 1 → 0.5 %.** Lost: 3.5 % for Euro 1 cars first used before 1/8/95 and outside the Annex. Euro 1 means a
  catalyst car, and a healthy catalyst car never needs 3.5 % to be "normal".
- **Euro 3 → 0.3 %.** Lost: 0.5 % for Euro 3 cars first used before 1/9/02 (about 20 months of registrations). The
  ceiling is for a healthy reading, and healthy cat cars idle far below 0.3 %.
- **Drop `hc_2500_ceiling`.** After R3 nothing reads it. Lost: keep it at 200 for all classes (dead data).
- **CAM_MAP floor 1.5 %, keep the CoC override.** Lost: also rework the `co_high_idle` override. That value is a CoC
  legal fast-idle limit, the same defect class, but only with HIGH-confidence DNA; it is registered as T-GASA-20.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | patch applied: `280 passed, 2 skipped, 4 deselected`; base code + new tests: 3 failed |
| step 2 | SIMULATED | patch applied: `610 passed` |
| step 3 | SIMULATED | patch applied: `510 passed, 5 skipped` |
| step 4 | SIMULATED | patch applied: `0`, `0` |
| step 5 | SIMULATED | patch applied: `All checks passed!` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-GASA-19: Euro idle CO to DVSA bands; CAM_MAP 2500 window HC 200-600, CO floor 1.5.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 0 findings (`C:/4DApp/recheck/scratch/coldread_T-GASA-19.md`). Second review on the result.

### Correction history ###
(none)
