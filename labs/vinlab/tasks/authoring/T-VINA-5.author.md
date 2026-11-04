# T-VINA-5 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Finding:** F-C6-2 (`audit/reports/R1_C6_20261017.md`); the probe `test_f2_make_matches_wmi_owner`.
2. **Measured (P2-P4)** with `recheck/T-VINA-5/measure.py` on fix/T-VINA-3 (2026-11-04): the wrong brands key their
   own engine-map rows; their shared `vds_full` keys with the right brand mostly disagree on the engine (MAYBACH /
   MERCEDES-BENZ 54 shared, 10 same engine). A rename would collide, so R2 needs a policy.
3. **Join:** `_resolve_engine` tries `EXACT_vds` then `FOLDED_vds` (`_fold_brand`); the brand comes from `wmi.csv`.
4. **Picked over T-VINA-10:** both are plan-gated; T-VINA-5 is blocked only by T-VINA-1 and touches data, not the
   diagnosis path (T-VINA-10 changes 36 corpus runs downstream).

### Rulings and the tradeoff that lost ###
- Plan REQUIRED, difficulty 4: the merge policy (R2) is a design choice with a measurable cost on real VINs.
- The engine-resolved floor (P3) is the guard. Lost: a census of the whole engine map: the real VINs are the
  population the app sees.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | base `229 passed, 8 skipped` (T-VINA-3 review); the plan sets the new count |
| step 2 | DEFERRED | the test file does not exist |
| step 3 | RAN | `27 passed`, `41 passed`, `30 passed` on fix/T-VINA-3 (T-VINA-3 review) |
| step 4 | RAN | base: 5 wrong-make pairs, engine resolved per P3 (Cowork, 2026-11-04) |
| step 5 | DEFERRED | ruff and the commits |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-5: five WMIs get their true make (WDB, KMH, JSA, JN1, SAX); engine-map join kept at or above P3.

### Cold read ###
own pass 2026-11-04: P1 grep 5 rows · P2-P4 measured · traceability: criteria 1-4 → steps 1-5 · JUDGEMENT: 0.
cold read 2026-11-04: skipped, plan-gated (Plan: REQUIRED; the plan review and its second-model review cover it).

### Correction history ###
