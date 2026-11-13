# T-COMA-21 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-11, F-C1-12; wiki 07 §CONCEPT_DEGRADATION_MODE, §RULE_LAB_SUPPRESSION;
wiki 09 §CONCEPT_CONF_TIER; `docs/COMLab_BDD.md` §0 and the "full fusion" / "single-point" / "legacy without a
scanner" scenarios. Rehearsal: `C:/4DApp/recheck/T-COMA-21/`.

### Verified context ###
1. **Still open on `8dc0b43`:** the four step-3 probes fail (cranking and no-OBD give `FULL_FUSION`; the clean
   ADAPTIVE request is `DEGRADED_ASSURANCE` at score 0.93; LEGACY vs MODERN give LOW vs HIGH at score 1.0). Observed.
2. **No scoring consumer of the mode:** the router and the shim copy `degradation_mode` into telemetry and the
   output; the UI displays it. Observed (`grep -rn degradation_mode` over comlab, registry, wired, ui).
3. **The two BDD scenarios conflict** for a clean four-lab request without a second frame ("full fusion" vs
   "single-point"); the BDD §0 table already lists SINGLE_POINT as delta-engine-only. Observed.
4. **Before, the rating was the era:** 302 LEGACY = LOW, 8 MODERN = HIGH, 1 ADAPTIVE = DEGRADED of 311; accuracy per
   tier did not order (HIGH 62 %, DEGRADED 100 %, LOW 70 %). After: HIGH 79 % (157/199), DEGRADED 73 % (8/11), LOW
   50 % (51/101). Verdicts `changed 0 of 314`; mode changed on 17. Observed (`meta.py` before and after).
5. **Rehearsal** (restored; `git apply --check` passes): comlab `527 → 538` (one regression fixture re-stated);
   wired `186`; ui `73`; step 2 `11 passed`, base `10 failed, 1 passed`; mutants A-E `1 failed` each; step 3
   `4 passed`; ruff clean; `4 files changed, 110 insertions(+), 23 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Mode = lab completeness.** Lost: emitting SINGLE_POINT whenever no second frame exists (it would label nearly
  every production session SINGLE_POINT and contradict the "full fusion" scenario; the delta engine keeps it).
- **Rating = score band, not era.** Lost: evidence-completeness wording in vocabulary.py (the wiki 09 rework
  redefines the tiers as score bands; P4 shows the band orders accuracy and the era did not).
- **GAS_DOMINANT caps the tier, not the score.** Lost: a score ceiling (changes verdicts and the corpus; a later
  calibration row).
- Plan NONE, difficulty 2 (contract, scripted). Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `540 passed, 4 skipped`; `186 passed`; `73 passed` |
| step 2 | SIMULATED | `13 passed` (correction 1); base `10 failed, 1 passed` |
| step 3 | SIMULATED | `4 passed` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `4 files changed, 126 insertions(+), 23 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-21: degradation_mode = lab completeness; rating = verdict score band, not era (F-C1-11/12).

### Cold read ###
own pass 2026-11-13: P1-P4 measured (facts 1, 4, 5) · patch applies clean · traceability: criteria 1-2 → steps 1-5
and R5 · cold read: not triggered (d2, scripted patch) · no finding.

### Correction history ###
- **Correction 1 (2026-11-13, second review of `3ed6cb0`, ds APPROVE WITH CORRECTIONS).** Upheld after
  re-derivation: (M) the docstring and BDD row drop the `suppress_gaslab` trigger; (L) the `suppress_gaslab`
  branch is untested; (L) no `process()` test of the GAS_DOMINANT cap; (L) "lab completeness" overclaims (the
  gate reads gas and OBD only). Not upheld: (M) porcelain evidence (Cowork ran `git status`: the note and the
  RESULT); (L) phase timings and the mutant-revert method (state verified by `cmp` and the restored stat).
  Rehearsed: step 2 `13 passed`; mutants F and G `1 failed, 12 passed`; comlab `540`; `4 files changed, 126
  insertions(+), 23 deletions(-)` from `8dc0b43`.
